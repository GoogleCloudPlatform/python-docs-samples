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

from datetime import datetime, timedelta, timezone
import runpy
from unittest import mock
import uuid

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_backups import copy_backup

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
BACKUP_ID = "example-copied-backup"
SOURCE_BACKUP = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/backups/example-src"
COPIED_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/backups/{BACKUP_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _fake_backup() -> spanner_admin_database_v1.Backup:
    return spanner_admin_database_v1.Backup(
        name=COPIED_NAME,
        state=spanner_admin_database_v1.Backup.State.READY,
        size_bytes=4096,
    )


@mock.patch(ADMIN_CLIENT)
def test_copy_backup_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.copy_backup.return_value.result.return_value = _fake_backup()

    copy_backup.copy_backup(PROJECT_ID, INSTANCE_ID, BACKUP_ID, SOURCE_BACKUP)

    req = client.copy_backup.call_args.kwargs["request"]
    assert req.backup_id == BACKUP_ID
    assert req.source_backup == SOURCE_BACKUP
    out, err = capsys.readouterr()
    assert f"Resource ID: {COPIED_NAME}" in out
    assert "Backup State: READY" in out
    assert "Size Bytes: 4096" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.AlreadyExists("exists"),
            "error: backup 'example-copied-backup' already exists",
        ),
        (
            exceptions.NotFound("missing"),
            "error: source backup",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to copy backup",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_copy_backup_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.copy_backup.side_effect = error

    copy_backup.copy_backup(PROJECT_ID, INSTANCE_ID, BACKUP_ID, SOURCE_BACKUP)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)


@mock.patch(ADMIN_CLIENT)
def test_copy_backup_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.copy_backup.return_value.result.return_value = _fake_backup()
    monkeypatch.setattr(
        "sys.argv",
        [
            "copy_backup.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--backup-id",
            BACKUP_ID,
            "--source-backup-path",
            SOURCE_BACKUP,
        ],
    )

    runpy.run_module("spanner_backups.copy_backup", run_name="__main__")

    assert "Backup State: READY" in capsys.readouterr().out


@conftest.live_only
def test_copy_backup_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    parent = admin.instance_path(conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID)
    suffix = uuid.uuid4().hex[:6]
    temp_db_id = f"example-bkp-db-{suffix}"
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        temp_db_id,
    )
    src_id = f"example-src-bkp-{suffix}"
    dst_id = f"example-cpy-bkp-{suffix}"
    src_name = f"{parent}/backups/{src_id}"
    dst_name = f"{parent}/backups/{dst_id}"

    try:
        admin.create_database(
            request=spanner_admin_database_v1.CreateDatabaseRequest(
                parent=parent,
                create_statement=f"CREATE DATABASE `{temp_db_id}`",
            )
        ).result(timeout=300)

        admin.create_backup(
            request=spanner_admin_database_v1.CreateBackupRequest(
                parent=parent,
                backup_id=src_id,
                backup=spanner_admin_database_v1.Backup(
                    database=db_path,
                    expire_time=datetime.now(timezone.utc) + timedelta(hours=8),
                ),
            )
        ).result(timeout=1800)

        copy_backup.copy_backup(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            dst_id,
            src_name,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert f"Resource ID: {dst_name}" in out
        assert "Backup State: READY" in out
    finally:
        for bkp in (dst_name, src_name):
            try:
                admin.delete_backup(name=bkp)
            except exceptions.NotFound:
                pass
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
