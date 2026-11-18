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
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_postgresql import postgresql_alter_sequence
from spanner_postgresql import postgresql_create_sequence
from spanner_postgresql import postgresql_drop_sequence

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-pg-db"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"
SPANNER_CLIENT = "google.cloud.spanner.Client"


def _setup_txn(mock_client_class: mock.MagicMock) -> mock.MagicMock:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    txn = mock.MagicMock()
    database.run_in_transaction.side_effect = lambda fn, *a, **kw: fn(txn)
    return txn


@mock.patch(SPANNER_CLIENT)
@mock.patch(ADMIN_CLIENT)
def test_alter_postgresql_sequence_success(
    mock_admin_class: mock.MagicMock,
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_admin_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_admin_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    txn = _setup_txn(mock_client_class)
    txn.execute_sql.return_value = [(6000001,), (6000002,), (6000003,)]

    postgresql_alter_sequence.alter_postgresql_sequence(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    req = mock_admin_class.return_value.update_database_ddl.call_args.kwargs["request"]
    assert req.statements == ["ALTER SEQUENCE Seq SKIP RANGE 1000 5000000"]
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Inserted Customers: 3" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (exceptions.NotFound("missing"), "error: database 'example-pg-db'"),
        (
            exceptions.FailedPrecondition("missing seq"),
            "error: failed to alter PostgreSQL sequence",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
@mock.patch(ADMIN_CLIENT)
def test_alter_postgresql_sequence_errors(
    mock_admin_class: mock.MagicMock,
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_admin_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_admin_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    mock_admin_class.return_value.update_database_ddl.side_effect = error

    postgresql_alter_sequence.alter_postgresql_sequence(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
@mock.patch(ADMIN_CLIENT)
def test_alter_postgresql_sequence_cli_entrypoint(
    mock_admin_class: mock.MagicMock,
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_admin_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_admin_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    txn = _setup_txn(mock_client_class)
    txn.execute_sql.return_value = [(6000001,), (6000002,), (6000003,)]
    monkeypatch.setattr(
        "sys.argv",
        [
            "postgresql_alter_sequence.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_postgresql.postgresql_alter_sequence", run_name="__main__"
    )

    assert "Inserted Customers: 3" in capsys.readouterr().out


@conftest.live_only
def test_alter_postgresql_sequence_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    admin.update_database_ddl(
        request={
            "database": db_path,
            "statements": [
                "DROP TABLE IF EXISTS Customers",
                "DROP SEQUENCE IF EXISTS Seq",
            ],
        }
    ).result(timeout=240)
    try:
        postgresql_create_sequence.create_postgresql_sequence(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        capsys.readouterr()
        postgresql_alter_sequence.alter_postgresql_sequence(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Inserted Customers: 3" in out
    finally:
        postgresql_drop_sequence.drop_postgresql_sequence(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        admin.update_database_ddl(
            request={
                "database": db_path,
                "statements": ["DROP TABLE IF EXISTS Customers"],
            }
        ).result(timeout=240)
