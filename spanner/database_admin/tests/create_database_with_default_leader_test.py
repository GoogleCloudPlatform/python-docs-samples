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
from spanner_database_admin import create_database_with_default_leader

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-mr-instance"
DATABASE_ID = "example-db"
DEFAULT_LEADER = "us-east4"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_database_with_default_leader_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock(default_leader=DEFAULT_LEADER)
    mock_client_class.return_value.create_database.return_value.result.return_value = (
        db_pb
    )

    create_database_with_default_leader.create_database_with_default_leader(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, DEFAULT_LEADER
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert f"Default Leader: {DEFAULT_LEADER}" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("dup"),
            "error: database 'example-db' already exists",
        ),
        (
            exceptions.InvalidArgument("bad leader"),
            "error: failed to create database 'example-db' with default leader",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_database_with_default_leader_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    mock_client_class.return_value.create_database.side_effect = error

    create_database_with_default_leader.create_database_with_default_leader(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID, DEFAULT_LEADER
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_database_with_default_leader_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.instance_path.return_value = (
        f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    )
    db_pb = mock.MagicMock(default_leader=DEFAULT_LEADER)
    mock_client_class.return_value.create_database.return_value.result.return_value = (
        db_pb
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_database_with_default_leader.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
            "--default-leader",
            DEFAULT_LEADER,
        ],
    )

    runpy.run_module(
        "spanner_database_admin.create_database_with_default_leader",
        run_name="__main__",
    )

    assert f"Default Leader: {DEFAULT_LEADER}" in capsys.readouterr().out


@conftest.live_only
def test_create_database_with_default_leader_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    mr_instance = os.environ["SPANNER_MR_INSTANCE_ID"]
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    temp_db_id = f"example-ldr-{uuid.uuid4().hex[:6]}"
    db_path = admin.database_path(conftest.LIVE_PROJECT_ID, mr_instance, temp_db_id)
    try:
        create_database_with_default_leader.create_database_with_default_leader(
            conftest.LIVE_PROJECT_ID, mr_instance, temp_db_id, "us-east4"
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Default Leader: us-east4" in out
    finally:
        try:
            admin.drop_database(database=db_path)
        except exceptions.NotFound:
            pass
