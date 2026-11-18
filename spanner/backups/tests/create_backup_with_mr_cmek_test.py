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
from spanner_backups import create_backup_with_mr_cmek

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-mr-instance"
DATABASE_ID = "example-mr-db"
BACKUP_ID = "example-mr-cmek-backup"
MR_KEYS = [
    f"projects/{PROJECT_ID}/locations/{loc}/keyRings/example-ring/cryptoKeys/example-key"
    for loc in ("us-central1", "us-east1", "us-east4")
]
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _setup_admin(mock_client_class: mock.MagicMock) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    client.database_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
    )
    bkp = mock.MagicMock(size_bytes=8192, encryption_information=[1, 2, 3])
    client.create_backup.return_value.result.return_value = bkp


@mock.patch(ADMIN_CLIENT)
def test_create_backup_with_mr_cmek_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    _setup_admin(mock_client_class)

    create_backup_with_mr_cmek.create_backup_with_mr_cmek(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, BACKUP_ID, MR_KEYS
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {BACKUP_ID}" in out
    assert "Encryption Info Entries: 3" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: backup 'example-mr-cmek-backup' already exists",
        ),
        (
            exceptions.FailedPrecondition("kms"),
            "error: failed to create multi-region CMEK backup",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_backup_with_mr_cmek_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _setup_admin(mock_client_class)
    mock_client_class.return_value.create_backup.side_effect = error

    create_backup_with_mr_cmek.create_backup_with_mr_cmek(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, BACKUP_ID, MR_KEYS
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_backup_with_mr_cmek_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_admin(mock_client_class)
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_backup_with_mr_cmek.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--backup-id",
            BACKUP_ID,
            "--kms-key-names",
            ",".join(MR_KEYS),
        ],
    )

    runpy.run_module("spanner_backups.create_backup_with_mr_cmek", run_name="__main__")

    assert "Encryption Info Entries: 3" in capsys.readouterr().out


@conftest.live_only
def test_create_backup_with_mr_cmek_live(capsys: pytest.CaptureFixture[str]) -> None:
    mr_inst = os.environ["SPANNER_MR_INSTANCE_ID"]
    mr_db = os.environ["SPANNER_MR_DATABASE_ID"]
    mr_keys = [k for k in os.environ["SPANNER_MR_KMS_KEY_NAMES"].split(",") if k]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    bkp_id = f"example-mrb-{uuid.uuid4().hex[:6]}"
    bkp_path = admin.backup_path(conftest.LIVE_PROJECT_ID, mr_inst, bkp_id)
    try:
        create_backup_with_mr_cmek.create_backup_with_mr_cmek(
            conftest.LIVE_PROJECT_ID, mr_inst, mr_db, bkp_id, mr_keys
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Encryption Info Entries:" in out
    finally:
        try:
            admin.delete_backup(name=bkp_path)
        except exceptions.NotFound:
            pass
