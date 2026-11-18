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
import pytest
from spanner_database_admin import list_databases

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_list_databases_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock()
    db_pb.name = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/example-db"
    db_pb.default_leader = "us-east4"
    mock_client_class.return_value.list_databases.return_value = [db_pb]

    list_databases.list_databases(PROJECT_ID, INSTANCE_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_ID}" in out
    assert "Database Count: 1" in out
    assert "Database ID: example-db, Default Leader: us-east4" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: instance 'example-instance'"),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to list databases on instance 'example-instance'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_list_databases_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.list_databases.side_effect = error

    list_databases.list_databases(PROJECT_ID, INSTANCE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_list_databases_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.list_databases.return_value = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "list_databases.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
        ],
    )

    runpy.run_module("spanner_database_admin.list_databases", run_name="__main__")

    assert "Database Count: 0" in capsys.readouterr().out


@conftest.live_only
def test_list_databases_live(capsys: pytest.CaptureFixture[str]) -> None:
    list_databases.list_databases(conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID)
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert f"Database ID: {conftest.LIVE_DATABASE_ID}" in out
