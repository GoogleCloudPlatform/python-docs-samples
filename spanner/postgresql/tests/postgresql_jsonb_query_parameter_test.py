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
from google.cloud import spanner_admin_database_v1
from google.cloud.spanner_v1 import JsonObject
import pytest
from spanner_postgresql import postgresql_jsonb_query_parameter

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-pg-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_query_postgresql_jsonb_parameter_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.return_value = [(19, '{"open": true, "rating": 9}')]

    postgresql_jsonb_query_parameter.query_postgresql_jsonb_parameter(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Row Count: 1" in out
    assert "Venue ID: 19" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: database 'example-pg-db'"),
        (
            exceptions.InvalidArgument("bad jsonb"),
            "error: PostgreSQL JSONB query failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_query_postgresql_jsonb_parameter_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.side_effect = error

    postgresql_jsonb_query_parameter.query_postgresql_jsonb_parameter(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_query_postgresql_jsonb_parameter_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.return_value = [(19, '{"open": true, "rating": 9}')]
    monkeypatch.setattr(
        "sys.argv",
        [
            "postgresql_jsonb_query_parameter.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_postgresql.postgresql_jsonb_query_parameter", run_name="__main__"
    )

    assert "Venue ID: 19" in capsys.readouterr().out


@conftest.live_only
def test_query_postgresql_jsonb_parameter_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
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
                "CREATE TABLE IF NOT EXISTS venues ("
                "  venueid bigint NOT NULL,"
                "  venuedetails jsonb,"
                "  PRIMARY KEY (venueid)"
                ")"
            ],
        }
    ).result(timeout=240)
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    db = client.instance(conftest.LIVE_INSTANCE_ID).database(conftest.LIVE_DATABASE_ID)
    with db.batch() as batch:
        batch.insert_or_update(
            table="venues",
            columns=("venueid", "venuedetails"),
            values=[(19, JsonObject(rating=9, open=True))],
        )
    postgresql_jsonb_query_parameter.query_postgresql_jsonb_parameter(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Venue ID: 19" in out
