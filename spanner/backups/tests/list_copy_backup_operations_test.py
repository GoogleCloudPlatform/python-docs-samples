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
from google.longrunning import operations_pb2
from google.protobuf import any_pb2
import pytest
from spanner_backups import list_copy_backup_operations

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
PARENT = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _fake_copy_op() -> operations_pb2.Operation:
    meta = spanner_admin_database_v1.CopyBackupMetadata(
        name=f"{PARENT}/backups/example-copied",
        source_backup=f"{PARENT}/backups/example-source",
    )
    packed = any_pb2.Any()
    packed.Pack(spanner_admin_database_v1.CopyBackupMetadata.pb(meta))
    return operations_pb2.Operation(
        name=f"{PARENT}/backups/example-copied/operations/op-1",
        metadata=packed,
        done=True,
    )


@mock.patch(ADMIN_CLIENT)
def test_list_copy_backup_operations_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = PARENT
    client.list_backup_operations.return_value = [_fake_copy_op()]

    list_copy_backup_operations.list_copy_backup_operations(PROJECT_ID, INSTANCE_ID)

    req = client.list_backup_operations.call_args.kwargs["request"]
    assert "CopyBackupMetadata" in req.filter
    out, err = capsys.readouterr()
    assert f"Resource ID: {PARENT}" in out
    assert "Copy Backup Operation Count: 1" in out
    assert f"Destination Backup: {PARENT}/backups/example-copied" in out
    assert "Operation Done: True" in out
    assert f"Source Backup: {PARENT}/backups/example-source" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("missing"),
            "error: Spanner instance 'example-instance'",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to list copy-backup operations",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_list_copy_backup_operations_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = PARENT
    client.list_backup_operations.side_effect = error

    list_copy_backup_operations.list_copy_backup_operations(PROJECT_ID, INSTANCE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)


@mock.patch(ADMIN_CLIENT)
def test_list_copy_backup_operations_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = PARENT
    client.list_backup_operations.return_value = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "list_copy_backup_operations.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
        ],
    )

    runpy.run_module("spanner_backups.list_copy_backup_operations", run_name="__main__")

    assert "Copy Backup Operation Count: 0" in capsys.readouterr().out


@conftest.live_only
def test_list_copy_backup_operations_live(capsys: pytest.CaptureFixture[str]) -> None:
    list_copy_backup_operations.list_copy_backup_operations(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Copy Backup Operation Count:" in out
