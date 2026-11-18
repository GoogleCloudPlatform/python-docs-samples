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
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_backups import create_backup

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
BACKUP_ID = "example-backup"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"
SPANNER_CLIENT = "google.cloud.spanner.Client"


def _setup_mocks(
    mock_admin_class: mock.MagicMock, mock_client_class: mock.MagicMock
) -> None:
    admin = mock_admin_class.return_value
    admin.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    admin.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    snap = (
        mock_client_class.return_value.instance.return_value.database.return_value.snapshot.return_value.__enter__.return_value
    )
    snap.execute_sql.return_value = [
        (datetime.datetime(2026, 1, 15, tzinfo=datetime.timezone.utc),)
    ]
    bkp = mock.MagicMock(size_bytes=4096)
    bkp.state.name = "READY"
    admin.create_backup.return_value.result.return_value = bkp


@mock.patch(SPANNER_CLIENT)
@mock.patch(ADMIN_CLIENT)
def test_create_backup_success(
    mock_admin_class: mock.MagicMock,
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_mocks(mock_admin_class, mock_client_class)

    create_backup.create_backup(PROJECT_ID, INSTANCE_ID, DATABASE_ID, BACKUP_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {BACKUP_ID}" in out
    assert "Backup Size Bytes: 4096" in out
    assert "Backup State: READY" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: backup 'example-backup' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to create backup 'example-backup'",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
@mock.patch(ADMIN_CLIENT)
def test_create_backup_errors(
    mock_admin_class: mock.MagicMock,
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _setup_mocks(mock_admin_class, mock_client_class)
    mock_admin_class.return_value.create_backup.side_effect = error

    create_backup.create_backup(PROJECT_ID, INSTANCE_ID, DATABASE_ID, BACKUP_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
@mock.patch(ADMIN_CLIENT)
def test_create_backup_cli_entrypoint(
    mock_admin_class: mock.MagicMock,
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_mocks(mock_admin_class, mock_client_class)
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_backup.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--backup-id",
            BACKUP_ID,
        ],
    )

    runpy.run_module("spanner_backups.create_backup", run_name="__main__")

    assert "Backup State: READY" in capsys.readouterr().out


@conftest.live_only
def test_create_backup_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    bkp_id = f"example-bkp-{uuid.uuid4().hex[:6]}"
    bkp_path = admin.backup_path(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, bkp_id
    )
    try:
        create_backup.create_backup(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
            bkp_id,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Backup State: READY" in out
    finally:
        try:
            admin.delete_backup(name=bkp_path)
        except exceptions.NotFound:
            pass
