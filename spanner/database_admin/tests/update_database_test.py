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
from spanner_database_admin import update_database

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_update_database_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    db_pb = mock.MagicMock(enable_drop_protection=True)
    mock_client_class.return_value.update_database.return_value.result.return_value = (
        db_pb
    )

    update_database.update_database(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Drop Protection Enabled: True" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (exceptions.NotFound("missing"), "error: database 'example-db'"),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to update database 'example-db'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_update_database_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    mock_client_class.return_value.update_database.side_effect = error

    update_database.update_database(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_update_database_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    db_pb = mock.MagicMock(enable_drop_protection=True)
    mock_client_class.return_value.update_database.return_value.result.return_value = (
        db_pb
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "update_database.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_database_admin.update_database", run_name="__main__")

    assert "Drop Protection Enabled: True" in capsys.readouterr().out


@conftest.live_only
def test_update_database_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    try:
        update_database.update_database(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Drop Protection Enabled: True" in out
    finally:
        admin.update_database(
            request=spanner_admin_database_v1.UpdateDatabaseRequest(
                database=spanner_admin_database_v1.Database(
                    name=db_path, enable_drop_protection=False
                ),
                update_mask={"paths": ["enable_drop_protection"]},
            )
        ).result(timeout=240)
