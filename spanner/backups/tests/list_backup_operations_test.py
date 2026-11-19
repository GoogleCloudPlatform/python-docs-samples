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
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_backups import list_backup_operations

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
BACKUP_ID = "example-backup"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _make_create_op() -> mock.MagicMock:
    meta = spanner_admin_database_v1.CreateBackupMetadata(
        name=f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/backups/{BACKUP_ID}",
        database=f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}",
        progress=spanner_admin_database_v1.OperationProgress(progress_percent=100),
    )
    op = mock.MagicMock()
    op.metadata.value = spanner_admin_database_v1.CreateBackupMetadata.serialize(meta)
    return op


@mock.patch(ADMIN_CLIENT)
def test_list_backup_operations_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.list_backup_operations.side_effect = [[_make_create_op()], []]

    list_backup_operations.list_backup_operations(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, BACKUP_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {INSTANCE_ID}" in out
    assert f"Create Backup ID: {BACKUP_ID}, Progress: 100%" in out
    assert "Create Operations Count: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: instance 'example-instance'"),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to list backup operations",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_list_backup_operations_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.list_backup_operations.side_effect = error

    list_backup_operations.list_backup_operations(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, BACKUP_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_list_backup_operations_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.list_backup_operations.side_effect = [[], []]
    monkeypatch.setattr(
        "sys.argv",
        [
            "list_backup_operations.py",
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

    runpy.run_module("spanner_backups.list_backup_operations", run_name="__main__")

    assert "Create Operations Count: 0" in capsys.readouterr().out


@conftest.live_only
def test_list_backup_operations_live(capsys: pytest.CaptureFixture[str]) -> None:
    required = ("SPANNER_BACKUP_ID",)
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    src_bkp = os.environ["SPANNER_BACKUP_ID"]
    list_backup_operations.list_backup_operations(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
        src_bkp,
    )
    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Create Operations Count:" in out
