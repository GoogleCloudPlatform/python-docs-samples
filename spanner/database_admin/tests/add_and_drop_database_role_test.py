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
from spanner_database_admin import add_and_drop_database_role

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_add_and_drop_database_role_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )

    add_and_drop_database_role.add_and_drop_database_role(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    assert mock_client_class.return_value.update_database_ddl.call_count == 2
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Active Role: new_parent" in out
    assert "Dropped Role: new_child" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.FailedPrecondition("exists"),
            "error: database role already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to manage database roles",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_add_and_drop_database_role_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    mock_client_class.return_value.update_database_ddl.side_effect = error

    add_and_drop_database_role.add_and_drop_database_role(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_add_and_drop_database_role_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "add_and_drop_database_role.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_database_admin.add_and_drop_database_role", run_name="__main__"
    )

    assert "Active Role: new_parent" in capsys.readouterr().out


@conftest.live_only
def test_add_and_drop_database_role_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    def cleanup_roles() -> None:
        for cleanup_stmt in [
            "REVOKE ROLE new_parent FROM ROLE new_child",
            "DROP ROLE new_child",
            "REVOKE SELECT ON TABLE Singers FROM ROLE new_parent",
            "DROP ROLE new_parent",
        ]:
            try:
                admin.update_database_ddl(
                    request={"database": db_path, "statements": [cleanup_stmt]}
                ).result(timeout=120)
            except exceptions.GoogleAPICallError:
                pass

    cleanup_roles()
    try:
        add_and_drop_database_role.add_and_drop_database_role(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Active Role: new_parent" in out
        assert "Dropped Role: new_child" in out
    finally:
        cleanup_roles()
