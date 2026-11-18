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
from google.cloud import spanner_v1
import pytest
from spanner_change_streams import read_change_stream

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SESSION_NAME = f"{DATABASE_NAME}/sessions/mux-1"
GAPIC_CLIENT = "google.cloud.spanner_v1.SpannerClient"


@mock.patch(GAPIC_CLIENT)
def test_read_change_stream_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.create_session.return_value = spanner_v1.Session(
        name=SESSION_NAME, multiplexed=True
    )
    client.execute_streaming_sql.return_value = [spanner_v1.PartialResultSet()]

    read_change_stream.read_change_stream(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    req = client.execute_streaming_sql.call_args.kwargs["request"]
    assert "READ_SingersAndAlbumsStream" in req.sql
    assert req.transaction.single_use.read_only.strong is True
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Change Stream: SingersAndAlbumsStream" in out
    assert "Stream Chunks Received: 1" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.InvalidArgument("bad stream"),
            "error: change stream read failed",
        ),
    ],
)
@mock.patch(GAPIC_CLIENT)
def test_read_change_stream_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.create_session.side_effect = error

    read_change_stream.read_change_stream(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(GAPIC_CLIENT)
def test_read_change_stream_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = mock_client_class.return_value
    client.create_session.return_value = spanner_v1.Session(
        name=SESSION_NAME, multiplexed=True
    )
    client.execute_streaming_sql.return_value = [spanner_v1.PartialResultSet()]
    monkeypatch.setattr(
        "sys.argv",
        [
            "read_change_stream.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_change_streams.read_change_stream", run_name="__main__")

    assert "Change Stream: SingersAndAlbumsStream" in capsys.readouterr().out


@conftest.live_only
def test_read_change_stream_live(capsys: pytest.CaptureFixture[str]) -> None:
    read_change_stream.read_change_stream(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Change Stream: SingersAndAlbumsStream" in out
    assert "Stream Chunks Received:" in out
