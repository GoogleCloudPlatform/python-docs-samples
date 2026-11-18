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
import uuid

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_postgresql import postgresql_add_column
from spanner_postgresql import postgresql_create_database

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-pg-db"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_add_postgresql_column_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    postgresql_add_column.add_postgresql_column(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    req = mock_client_class.return_value.update_database_ddl.call_args.kwargs["request"]
    assert req.statements == ["ALTER TABLE Albums ADD COLUMN MarketingBudget BIGINT"]
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Added Column: MarketingBudget" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.FailedPrecondition("exists"),
            "error: column 'MarketingBudget' already exists",
        ),
        (
            TimeoutError("deadline"),
            "error: timed out waiting to add column 'MarketingBudget'",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to add column 'MarketingBudget'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_add_postgresql_column_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    mock_client_class.return_value.update_database_ddl.side_effect = error

    postgresql_add_column.add_postgresql_column(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_add_postgresql_column_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "postgresql_add_column.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_postgresql.postgresql_add_column", run_name="__main__")

    assert "Added Column: MarketingBudget" in capsys.readouterr().out


@conftest.live_only
def test_add_postgresql_column_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    temp_db_id = f"example-pgcol-{uuid.uuid4().hex[:5]}"
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
    )
    try:
        postgresql_create_database.create_postgresql_database(
            conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
        )
        capsys.readouterr()
        postgresql_add_column.add_postgresql_column(
            conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Added Column: MarketingBudget" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
