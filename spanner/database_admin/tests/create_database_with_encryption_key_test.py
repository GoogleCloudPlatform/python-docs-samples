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
from spanner_database_admin import create_database_with_encryption_key

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-cmek-db"
KMS_KEY = f"projects/{PROJECT_ID}/locations/us-central1/keyRings/example-ring/cryptoKeys/example-key"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_database_with_encryption_key_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock()
    db_pb.encryption_config.kms_key_name = KMS_KEY
    mock_client_class.return_value.create_database.return_value.result.return_value = (
        db_pb
    )

    create_database_with_encryption_key.create_database_with_encryption_key(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, KMS_KEY
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Encryption Key ID: example-key" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: database 'example-cmek-db' already exists",
        ),
        (
            exceptions.FailedPrecondition("kms"),
            "error: failed to create CMEK database 'example-cmek-db'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_database_with_encryption_key_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.create_database.side_effect = error

    create_database_with_encryption_key.create_database_with_encryption_key(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, KMS_KEY
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_database_with_encryption_key_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock()
    db_pb.encryption_config.kms_key_name = KMS_KEY
    mock_client_class.return_value.create_database.return_value.result.return_value = (
        db_pb
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_database_with_encryption_key.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--kms-key-name",
            KMS_KEY,
        ],
    )

    runpy.run_module(
        "spanner_database_admin.create_database_with_encryption_key",
        run_name="__main__",
    )

    assert "Encryption Key ID: example-key" in capsys.readouterr().out


@conftest.live_only
def test_create_database_with_encryption_key_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    kms_key = os.environ["SPANNER_KMS_KEY_NAME"]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    temp_db_id = f"example-cmk-{uuid.uuid4().hex[:6]}"
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID, conftest.LIVE_INSTANCE_ID, temp_db_id
    )
    try:
        create_database_with_encryption_key.create_database_with_encryption_key(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            temp_db_id,
            kms_key,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Encryption Key ID:" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
