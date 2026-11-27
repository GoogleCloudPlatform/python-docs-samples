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
import pytest
from spanner_change_streams import create_change_stream

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_PATH = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_change_stream_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH

    create_change_stream.create_change_stream(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    req = client.update_database_ddl.call_args.kwargs["request"]
    assert "CREATE CHANGE STREAM NamesAndAlbumsStream" in req.statements[0]
    assert "allow_txn_exclusion = true" in req.statements[0]
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Change Stream: NamesAndAlbumsStream" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.FailedPrecondition("duplicate"),
            "error: change stream 'NamesAndAlbumsStream' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to create change stream 'NamesAndAlbumsStream'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_change_stream_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH
    client.update_database_ddl.side_effect = error

    create_change_stream.create_change_stream(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_change_stream_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.database_path.return_value = DATABASE_PATH
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_change_stream.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_change_streams.create_change_stream", run_name="__main__")

    assert "Change Stream: NamesAndAlbumsStream" in capsys.readouterr().out


@conftest.live_only
def test_create_change_stream_live(capsys: pytest.CaptureFixture[str]) -> None:
    admin = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    try:
        admin.update_database_ddl(
            request={
                "database": db_path,
                "statements": ["DROP CHANGE STREAM NamesAndAlbumsStream"],
            }
        ).result(timeout=180)
    except (exceptions.NotFound, exceptions.FailedPrecondition):
        pass

    try:
        create_change_stream.create_change_stream(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert "Change Stream: NamesAndAlbumsStream" in out
    finally:
        try:
            admin.update_database_ddl(
                request={
                    "database": db_path,
                    "statements": ["DROP CHANGE STREAM NamesAndAlbumsStream"],
                }
            ).result(timeout=180)
        except (exceptions.NotFound, exceptions.FailedPrecondition):
            pass
