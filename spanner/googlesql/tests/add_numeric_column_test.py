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
from spanner_googlesql import add_numeric_column

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_PATH = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_add_numeric_column_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH

    add_numeric_column.add_numeric_column(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    req = client.update_database_ddl.call_args.kwargs["request"]
    assert req.statements == ["ALTER TABLE Venues ADD COLUMN Revenue NUMERIC"]
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Added Column: Revenue" in out
    assert "Table Name: Venues" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.FailedPrecondition("Duplicate column"),
            "error: column 'Revenue' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to add column 'Revenue'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_add_numeric_column_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH
    client.update_database_ddl.side_effect = error

    add_numeric_column.add_numeric_column(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_add_numeric_column_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.database_path.return_value = DATABASE_PATH
    monkeypatch.setattr(
        "sys.argv",
        [
            "add_numeric_column.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_googlesql.add_numeric_column", run_name="__main__")

    assert "Added Column: Revenue" in capsys.readouterr().out


@conftest.live_only
def test_add_numeric_column_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    parent = admin.instance_path(conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID)
    temp_db_id = f"example-num-{uuid.uuid4().hex[:6]}"
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
    )
    try:
        admin.create_database(
            request=spanner_admin_database_v1.CreateDatabaseRequest(
                parent=parent,
                create_statement=f"CREATE DATABASE `{temp_db_id}`",
                extra_statements=["""
                    CREATE TABLE Venues (
                      VenueId INT64 NOT NULL,
                      VenueName STRING(1024)
                    ) PRIMARY KEY (VenueId)
                """],
            )
        ).result(timeout=300)

        add_numeric_column.add_numeric_column(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            temp_db_id,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Resource ID: {temp_db_id}" in out
        assert "Added Column: Revenue" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
