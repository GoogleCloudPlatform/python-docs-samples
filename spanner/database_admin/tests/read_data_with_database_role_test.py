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
from spanner_database_admin import read_data_with_database_role

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_read_data_with_database_role_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    instance = mock_client_class.return_value.instance.return_value
    snapshot = (
        instance.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.return_value = [(1, "Marc", "Richards")]

    read_data_with_database_role.read_data_with_database_role(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    instance.database.assert_called_once_with(DATABASE_ID, database_role="new_parent")
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Database Role: new_parent" in out
    assert "Row Count: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.PermissionDenied("denied"),
            "error: database role 'new_parent' lacks SELECT access",
        ),
        (
            exceptions.NotFound("missing"),
            "error: query with database role 'new_parent' failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_read_data_with_database_role_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.side_effect = error

    read_data_with_database_role.read_data_with_database_role(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_read_data_with_database_role_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snapshot.execute_sql.return_value = [(1, "Marc", "Richards")]
    monkeypatch.setattr(
        "sys.argv",
        [
            "read_data_with_database_role.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_database_admin.read_data_with_database_role", run_name="__main__"
    )

    assert "Row Count: 1" in capsys.readouterr().out


@conftest.live_only
def test_read_data_with_database_role_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    try:
        admin.update_database_ddl(
            request={
                "database": db_path,
                "statements": [
                    "CREATE ROLE new_parent",
                    "GRANT SELECT ON TABLE Singers TO ROLE new_parent",
                ],
            }
        ).result(timeout=120)
    except exceptions.GoogleAPICallError:
        pass

    read_data_with_database_role.read_data_with_database_role(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Database Role: new_parent" in out
    assert "Marc Richards" in out
