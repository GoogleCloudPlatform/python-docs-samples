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
from spanner_backups import copy_backup_with_mr_cmek

from . import conftest

PROJECT_ID = "example-project-id"
DST_INST = "example-mr-instance"
DST_BKP = "example-copied-mr-backup"
SRC_INST = "example-instance"
SRC_BKP = "example-source-backup"
MR_KEYS = [
    f"projects/{PROJECT_ID}/locations/{loc}/keyRings/example-ring/cryptoKeys/example-key"
    for loc in ("us-central1", "us-east1", "us-east4")
]
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


def _setup_admin(mock_client_class: mock.MagicMock) -> None:
    client = mock_client_class.return_value
    client.instance_path.return_value = f"projects/{PROJECT_ID}/instances/{DST_INST}"
    client.backup_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{SRC_INST}/backups/{SRC_BKP}"
    )
    copied = mock.MagicMock(size_bytes=8192, encryption_information=[1, 2, 3])
    client.copy_backup.return_value.result.return_value = copied


@mock.patch(ADMIN_CLIENT)
def test_copy_backup_with_mr_cmek_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    _setup_admin(mock_client_class)

    copy_backup_with_mr_cmek.copy_backup_with_mr_cmek(
        PROJECT_ID, DST_INST, DST_BKP, SRC_INST, SRC_BKP, MR_KEYS
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DST_BKP}" in out
    assert "Encryption Info Entries: 3" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: destination backup 'example-copied-mr-backup' already exists",
        ),
        (
            exceptions.FailedPrecondition("kms"),
            "error: failed to copy backup 'example-source-backup'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_copy_backup_with_mr_cmek_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    _setup_admin(mock_client_class)
    mock_client_class.return_value.copy_backup.side_effect = error

    copy_backup_with_mr_cmek.copy_backup_with_mr_cmek(
        PROJECT_ID, DST_INST, DST_BKP, SRC_INST, SRC_BKP, MR_KEYS
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_copy_backup_with_mr_cmek_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _setup_admin(mock_client_class)
    monkeypatch.setattr(
        "sys.argv",
        [
            "copy_backup_with_mr_cmek.py",
            "--project-id",
            PROJECT_ID,
            "--destination-instance-id",
            DST_INST,
            "--destination-backup-id",
            DST_BKP,
            "--source-instance-id",
            SRC_INST,
            "--source-backup-id",
            SRC_BKP,
            "--kms-key-names",
            ",".join(MR_KEYS),
        ],
    )

    runpy.run_module("spanner_backups.copy_backup_with_mr_cmek", run_name="__main__")

    assert "Encryption Info Entries: 3" in capsys.readouterr().out


@conftest.live_only
def test_copy_backup_with_mr_cmek_live(capsys: pytest.CaptureFixture[str]) -> None:
    required = (
        "SPANNER_MR_INSTANCE_ID",
        "SPANNER_BACKUP_ID",
        "SPANNER_MR_KMS_KEY_NAMES",
    )
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    mr_inst = os.environ["SPANNER_MR_INSTANCE_ID"]
    src_bkp = os.environ["SPANNER_BACKUP_ID"]
    mr_keys = [k for k in os.environ["SPANNER_MR_KMS_KEY_NAMES"].split(",") if k]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    dst_bkp = f"example-cpb-{uuid.uuid4().hex[:6]}"
    dst_path = admin.backup_path(conftest.LIVE_PROJECT_ID, mr_inst, dst_bkp)
    try:
        copy_backup_with_mr_cmek.copy_backup_with_mr_cmek(
            conftest.LIVE_PROJECT_ID,
            mr_inst,
            dst_bkp,
            conftest.LIVE_INSTANCE_ID,
            src_bkp,
            mr_keys,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Resource ID: {dst_bkp}" in out
    finally:
        try:
            admin.delete_backup(name=dst_path)
        except exceptions.NotFound:
            pass
