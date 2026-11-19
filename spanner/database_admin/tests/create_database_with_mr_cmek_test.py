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
from spanner_database_admin import create_database_with_mr_cmek

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-mr-instance"
DATABASE_ID = "example-mr-cmek-db"
MR_KEYS = [
    f"projects/{PROJECT_ID}/locations/{loc}/keyRings/example-ring/cryptoKeys/example-key"
    for loc in ("us-central1", "us-east1", "us-east4")
]
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_database_with_mr_cmek_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock()
    db_pb.encryption_config.kms_key_names = MR_KEYS
    mock_client_class.return_value.create_database.return_value.result.return_value = (
        db_pb
    )

    create_database_with_mr_cmek.create_database_with_mr_cmek(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, MR_KEYS
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Configured KMS Keys: 3" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: database 'example-mr-cmek-db' already exists",
        ),
        (
            exceptions.FailedPrecondition("kms"),
            "error: failed to create multi-region CMEK database",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_database_with_mr_cmek_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.create_database.side_effect = error

    create_database_with_mr_cmek.create_database_with_mr_cmek(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, MR_KEYS
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_database_with_mr_cmek_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock()
    db_pb.encryption_config.kms_key_names = MR_KEYS
    mock_client_class.return_value.create_database.return_value.result.return_value = (
        db_pb
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_database_with_mr_cmek.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--kms-key-names",
            ",".join(MR_KEYS),
        ],
    )

    runpy.run_module(
        "spanner_database_admin.create_database_with_mr_cmek", run_name="__main__"
    )

    assert "Configured KMS Keys: 3" in capsys.readouterr().out


@conftest.live_only
def test_create_database_with_mr_cmek_live(capsys: pytest.CaptureFixture[str]) -> None:
    required = ("SPANNER_MR_INSTANCE_ID", "SPANNER_MR_KMS_KEY_NAMES")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"Set {', '.join(missing)} to run this live test.")
    mr_instance = os.environ["SPANNER_MR_INSTANCE_ID"]
    mr_keys = [k for k in os.environ["SPANNER_MR_KMS_KEY_NAMES"].split(",") if k]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    temp_db_id = f"example-mrc-{uuid.uuid4().hex[:6]}"
    db_path = admin.database_path(conftest.LIVE_PROJECT_ID, mr_instance, temp_db_id)
    try:
        create_database_with_mr_cmek.create_database_with_mr_cmek(
            conftest.LIVE_PROJECT_ID, mr_instance, temp_db_id, mr_keys
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert f"Configured KMS Keys: {len(mr_keys)}" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
