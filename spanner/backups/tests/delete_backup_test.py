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

from google.api_core import exceptions
import pytest
from spanner_backups import delete_backup

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
BACKUP_ID = "example-backup"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _setup_admin(mock_client_class: mock.MagicMock) -> None:
    client = mock_client_class.return_value
    client.backup_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/backups/{BACKUP_ID}"
    )
    client.get_backup.return_value.referencing_databases = []


@mock.patch(ADMIN_CLIENT)
def test_delete_backup_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    _setup_admin(mock_client_class)

    delete_backup.delete_backup(PROJECT_ID, INSTANCE_ID, BACKUP_ID)

    mock_client_class.return_value.delete_backup.assert_called_once()
    out, err = capsys.readouterr()
    assert f"Resource ID: {BACKUP_ID}" in out
    assert f"Deleted Backup: {BACKUP_ID}" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: backup 'example-backup'"),
        (
            exceptions.FailedPrecondition("in use"),
            "error: failed to delete backup 'example-backup'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_delete_backup_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _setup_admin(mock_client_class)
    mock_client_class.return_value.delete_backup.side_effect = error

    delete_backup.delete_backup(PROJECT_ID, INSTANCE_ID, BACKUP_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_delete_backup_times_out_while_referenced(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    _setup_admin(mock_client_class)
    client = mock_client_class.return_value
    client.get_backup.return_value.referencing_databases = ["restored-db"]

    with mock.patch.object(delete_backup, "time") as mock_time:
        mock_time.monotonic.side_effect = [0.0, 2000.0]
        delete_backup.delete_backup(PROJECT_ID, INSTANCE_ID, BACKUP_ID)

    client.delete_backup.assert_not_called()
    out, err = capsys.readouterr()
    assert f"Waiting for backup '{BACKUP_ID}' to be unreferenced..." in out
    assert err.startswith(f"error: timed out waiting to delete backup '{BACKUP_ID}'")
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_delete_backup_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_admin(mock_client_class)
    monkeypatch.setattr(
        "sys.argv",
        [
            "delete_backup.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--backup-id",
            BACKUP_ID,
        ],
    )

    runpy.run_module("spanner_backups.delete_backup", run_name="__main__")

    assert f"Deleted Backup: {BACKUP_ID}" in capsys.readouterr().out


@conftest.live_only
def test_delete_backup_live(capsys: pytest.CaptureFixture[str]) -> None:
    required = ("SPANNER_DISPOSABLE_BACKUP_ID",)
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    disposable_bkp = os.environ["SPANNER_DISPOSABLE_BACKUP_ID"]
    delete_backup.delete_backup(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        disposable_bkp,
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert f"Deleted Backup: {disposable_bkp}" in out
