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
from spanner_postgresql import postgresql_dml_last_statement

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-pg-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_update_postgresql_dml_last_statement_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_update.return_value = 1
    database.run_in_transaction.side_effect = lambda fn: fn(transaction)

    postgresql_dml_last_statement.update_postgresql_dml_last_statement(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    call = transaction.execute_update.call_args
    assert "$1" in call.args[0]
    assert call.kwargs["last_statement"] is True
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Last Statement Optimization: True" in out
    assert "Updated Rows: 1" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: PostgreSQL database 'example-pg-db' on instance",
        ),
        (
            exceptions.Aborted("aborted"),
            "error: PostgreSQL DML last_statement update failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_update_postgresql_dml_last_statement_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    postgresql_dml_last_statement.update_postgresql_dml_last_statement(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_update_postgresql_dml_last_statement_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_update.return_value = 1
    database.run_in_transaction.side_effect = lambda fn: fn(transaction)
    monkeypatch.setattr(
        "sys.argv",
        [
            "postgresql_dml_last_statement.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_postgresql.postgresql_dml_last_statement", run_name="__main__"
    )

    assert "Updated Rows: 1" in capsys.readouterr().out


@conftest.live_only
def test_update_postgresql_dml_last_statement_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    database = client.instance(conftest.LIVE_INSTANCE_ID).database(
        conftest.LIVE_DATABASE_ID
    )
    database.run_in_transaction(
        lambda txn: txn.execute_update(
            "INSERT INTO Singers (SingerId, FirstName, LastName) "
            "VALUES (54214, 'John', 'Smith') "
            "ON CONFLICT (SingerId) DO UPDATE SET LastName = 'Smith'"
        )
    )
    try:
        postgresql_dml_last_statement.update_postgresql_dml_last_statement(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )

        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Last Statement Optimization: True" in out
        assert "Updated Rows: 1" in out
    finally:
        database.run_in_transaction(
            lambda txn: txn.execute_update("DELETE FROM Singers WHERE SingerId = 54214")
        )
