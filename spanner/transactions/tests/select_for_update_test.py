# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Callable
import runpy
from unittest import mock

from google.api_core import exceptions
from google.cloud import spanner_v1
import pytest
from spanner_transactions import select_for_update

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_transfer_budget_with_select_for_update_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_sql.side_effect = [
        [(500000,)],
        [(None,)],
    ]

    def run_txn(
        fn: Callable[[mock.MagicMock], None],
        isolation_level: spanner_v1.TransactionOptions.IsolationLevel,
    ) -> None:
        assert (
            isolation_level
            == spanner_v1.TransactionOptions.IsolationLevel.REPEATABLE_READ
        )
        fn(transaction)

    database.run_in_transaction.side_effect = run_txn

    select_for_update.transfer_budget_with_select_for_update(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    first_sql = transaction.execute_sql.call_args_list[0].args[0]
    assert "FOR UPDATE" in first_sql
    assert transaction.execute_update.call_count == 2

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Source Budget: 490000" in out
    assert "Target Budget: 10000" in out
    assert err == ""


@mock.patch(SPANNER_CLIENT)
def test_transfer_budget_with_select_for_update_missing_album(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    transaction = mock.MagicMock()
    transaction.execute_sql.side_effect = [[], [(300000,)]]
    database.run_in_transaction.side_effect = lambda fn, **_kw: fn(transaction)

    select_for_update.transfer_budget_with_select_for_update(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert "Source or target album row was not found." in err


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.Aborted("aborted"),
            "error: SELECT FOR UPDATE transaction failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_transfer_budget_with_select_for_update_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    select_for_update.transfer_budget_with_select_for_update(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_transfer_budget_with_select_for_update_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_sql.side_effect = [[(500000,)], [(300000,)]]
    database.run_in_transaction.side_effect = lambda fn, **_kw: fn(transaction)
    monkeypatch.setattr(
        "sys.argv",
        [
            "select_for_update.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_transactions.select_for_update", run_name="__main__")

    assert "Source Budget: 490000" in capsys.readouterr().out


@conftest.live_only
def test_transfer_budget_with_select_for_update_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    select_for_update.transfer_budget_with_select_for_update(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Source Budget:" in out
    assert "Target Budget:" in out
