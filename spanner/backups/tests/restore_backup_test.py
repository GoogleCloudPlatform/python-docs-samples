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

import os
import runpy
from unittest import mock
import uuid

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_backups import restore_backup

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
NEW_DB_ID = "example-restored-db"
BACKUP_ID = "example-backup"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _setup_admin(mock_client_class: mock.MagicMock) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.backup_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/backups/{BACKUP_ID}"
    )
    db_pb = mock.MagicMock()
    db_pb.restore_info.backup_info.source_database = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/example-db"
    )
    client.restore_database.return_value.result.return_value = db_pb


@mock.patch(ADMIN_CLIENT)
def test_restore_backup_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    _setup_admin(mock_client_class)

    restore_backup.restore_backup(PROJECT_ID, INSTANCE_ID, NEW_DB_ID, BACKUP_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {NEW_DB_ID}" in out
    assert f"Restored From Backup: {BACKUP_ID}" in out
    assert "Source Database ID: example-db" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: target database 'example-restored-db' already exists",
        ),
        (
            exceptions.NotFound("missing"),
            "error: failed to restore backup 'example-backup'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_restore_backup_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _setup_admin(mock_client_class)
    mock_client_class.return_value.restore_database.side_effect = error

    restore_backup.restore_backup(PROJECT_ID, INSTANCE_ID, NEW_DB_ID, BACKUP_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_restore_backup_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_admin(mock_client_class)
    monkeypatch.setattr(
        "sys.argv",
        [
            "restore_backup.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--new-database-id",
            NEW_DB_ID,
            "--backup-id",
            BACKUP_ID,
        ],
    )

    runpy.run_module("spanner_backups.restore_backup", run_name="__main__")

    assert "Source Database ID: example-db" in capsys.readouterr().out


@conftest.live_only
def test_restore_backup_live(capsys: pytest.CaptureFixture[str]) -> None:
    src_bkp = os.environ["SPANNER_BACKUP_ID"]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    new_db = f"example-rst-{uuid.uuid4().hex[:6]}"
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, new_db
    )
    try:
        restore_backup.restore_backup(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            new_db,
            src_bkp,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Resource ID: {new_db}" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
