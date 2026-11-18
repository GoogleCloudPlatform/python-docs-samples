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
from spanner_backups import create_full_backup_schedule
from spanner_backups import delete_backup_schedule

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SCHEDULE_ID = "example-backup-schedule"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _setup_admin(mock_client_class: mock.MagicMock) -> None:
    mock_client_class.return_value.backup_schedule_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
        f"/databases/{DATABASE_ID}/backupSchedules/{SCHEDULE_ID}"
    )


@mock.patch(ADMIN_CLIENT)
def test_delete_backup_schedule_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    _setup_admin(mock_client_class)

    delete_backup_schedule.delete_backup_schedule(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, SCHEDULE_ID
    )

    mock_client_class.return_value.delete_backup_schedule.assert_called_once()
    out, err = capsys.readouterr()
    assert f"Resource ID: {SCHEDULE_ID}" in out
    assert f"Deleted Schedule: {SCHEDULE_ID}" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("missing"),
            "error: backup schedule 'example-backup-schedule'",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to delete backup schedule",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_delete_backup_schedule_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _setup_admin(mock_client_class)
    mock_client_class.return_value.delete_backup_schedule.side_effect = error

    delete_backup_schedule.delete_backup_schedule(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, SCHEDULE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_delete_backup_schedule_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_admin(mock_client_class)
    monkeypatch.setattr(
        "sys.argv",
        [
            "delete_backup_schedule.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--schedule-id",
            SCHEDULE_ID,
        ],
    )

    runpy.run_module("spanner_backups.delete_backup_schedule", run_name="__main__")

    assert f"Deleted Schedule: {SCHEDULE_ID}" in capsys.readouterr().out


@conftest.live_only
def test_delete_backup_schedule_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    sid = f"example-dsc-{uuid.uuid4().hex[:6]}"
    spath = admin.backup_schedule_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
        sid,
    )
    try:
        create_full_backup_schedule.create_full_backup_schedule(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
            sid,
        )
        capsys.readouterr()
        delete_backup_schedule.delete_backup_schedule(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
            sid,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Deleted Schedule: {sid}" in out
    finally:
        try:
            admin.delete_backup_schedule(name=spath)
        except exceptions.NotFound:
            pass
