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
from spanner_googlesql import insert_data

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_insert_data_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    batch = database.batch.return_value.__enter__.return_value

    insert_data.insert_data(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    assert batch.insert.call_count == 2
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Inserted Albums: 5" in out
    assert "Inserted Singers: 5" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.AlreadyExists("dup"),
            "error: one or more Singers or Albums rows already exist",
        ),
        (exceptions.NotFound("missing"), "error: batch insert failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_insert_data_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.batch.return_value.__enter__.side_effect = error

    insert_data.insert_data(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_insert_data_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "insert_data.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_googlesql.insert_data", run_name="__main__")

    assert "Inserted Singers: 5" in capsys.readouterr().out


@conftest.live_only
def test_insert_data_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    parent = admin.instance_path(conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID)
    temp_db_id = f"example-ins-{uuid.uuid4().hex[:6]}"
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

        insert_data.insert_data(
            conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Inserted Albums: 5" in out
        assert "Inserted Singers: 5" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
