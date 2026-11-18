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

import datetime
import runpy
from unittest import mock
import uuid

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_googlesql import delete_data

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_delete_data_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    batch = database.batch.return_value.__enter__.return_value
    batch.committed = datetime.datetime(
        2026, 1, 15, 12, 0, tzinfo=datetime.timezone.utc
    )

    delete_data.delete_data(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    assert batch.delete.call_count == 3
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Committed At: 2026-01-15T12:00:00+00:00" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: database 'example-db'"),
        (exceptions.PermissionDenied("denied"), "error: batch delete failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_delete_data_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.batch.return_value.__enter__.side_effect = error

    delete_data.delete_data(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_delete_data_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.batch.return_value.__enter__.return_value.committed = datetime.datetime(
        2026, 1, 15, 12, 0, tzinfo=datetime.timezone.utc
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "delete_data.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_googlesql.delete_data", run_name="__main__")

    assert "Committed At: 2026-01-15T12:00:00+00:00" in capsys.readouterr().out


@conftest.live_only
def test_delete_data_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    parent = admin.instance_path(conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID)
    temp_db_id = f"example-del-{uuid.uuid4().hex[:6]}"
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
    )
    try:
        admin.create_database(
            request=spanner_admin_database_v1.CreateDatabaseRequest(
                parent=parent,
                create_statement=f"CREATE DATABASE `{temp_db_id}`",
                extra_statements=[
                    "CREATE TABLE Singers ("
                    "  SingerId INT64 NOT NULL,"
                    "  FirstName STRING(1024),"
                    "  LastName STRING(1024)"
                    ") PRIMARY KEY (SingerId)",
                    "CREATE TABLE Albums ("
                    "  SingerId INT64 NOT NULL,"
                    "  AlbumId INT64 NOT NULL,"
                    "  AlbumTitle STRING(MAX)"
                    ") PRIMARY KEY (SingerId, AlbumId),"
                    "  INTERLEAVE IN PARENT Singers ON DELETE CASCADE",
                ],
            )
        ).result(timeout=300)

        client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
        temp_db = client.instance(conftest.LIVE_INSTANCE_ID).database(temp_db_id)
        with temp_db.batch() as batch:
            batch.insert(
                table="Singers",
                columns=("SingerId", "FirstName", "LastName"),
                values=[
                    (1, "Marc", "Richards"),
                    (2, "Catalina", "Smith"),
                    (3, "Alice", "Trentor"),
                ],
            )
            batch.insert(
                table="Albums",
                columns=("SingerId", "AlbumId", "AlbumTitle"),
                values=[(2, 1, "Green"), (2, 3, "Terrified")],
            )

        delete_data.delete_data(
            conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Committed At:" in out

        with temp_db.snapshot() as snap:
            remaining = list(snap.execute_sql("SELECT COUNT(*) FROM Singers"))
            assert remaining[0][0] == 0
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
