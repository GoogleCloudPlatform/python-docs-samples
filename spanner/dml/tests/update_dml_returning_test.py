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

import runpy
from unittest import mock

from google.api_core import exceptions
from google.cloud import spanner
import pytest
from spanner_dml import update_dml_returning

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


def _mock_result_set(rows: list[tuple[object, ...]], count: int) -> mock.MagicMock:
    rs = mock.MagicMock()
    rs.__iter__.return_value = iter(rows)
    rs.stats.row_count_exact = count
    return rs


@mock.patch(SPANNER_CLIENT)
def test_update_dml_returning_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_sql.return_value = _mock_result_set([(200000,)], 1)
    database.run_in_transaction.side_effect = lambda fn: fn(transaction)

    update_dml_returning.update_dml_returning(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    sql = transaction.execute_sql.call_args.args[0]
    assert "THEN RETURN MarketingBudget" in sql
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Marketing Budget: 200000" in out
    assert "Updated Rows: 1" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.Aborted("aborted"),
            "error: UPDATE DML RETURNING failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_update_dml_returning_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    update_dml_returning.update_dml_returning(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_update_dml_returning_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_sql.return_value = _mock_result_set([(200000,)], 1)
    database.run_in_transaction.side_effect = lambda fn: fn(transaction)
    monkeypatch.setattr(
        "sys.argv",
        [
            "update_dml_returning.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_dml.update_dml_returning", run_name="__main__")

    assert "Marketing Budget: 200000" in capsys.readouterr().out


@conftest.live_only
def test_update_dml_returning_live(capsys: pytest.CaptureFixture[str]) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    database = client.instance(conftest.LIVE_INSTANCE_ID).database(
        conftest.LIVE_DATABASE_ID
    )
    with database.batch() as batch:
        batch.update(
            table="Albums",
            columns=("SingerId", "AlbumId", "MarketingBudget"),
            values=[(1, 1, 100000)],
        )

    update_dml_returning.update_dml_returning(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Marketing Budget: 200000" in out
    assert "Updated Rows: 1" in out
