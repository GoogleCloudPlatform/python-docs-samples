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

from datetime import datetime, timedelta, timezone
import runpy
from unittest import mock

from google.api_core import exceptions
import pytest
from spanner_queues import queue_receive_messages
from spanner_queues import queue_send_message

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_receive_and_ack_queue_messages_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    future_lease = datetime.now(timezone.utc) + timedelta(seconds=10)
    expired_lease = datetime.now(timezone.utc) - timedelta(seconds=10)
    snapshot.execute_sql.return_value = [
        (1, "msg-valid", b"payload-1", future_lease),
        (1, "msg-expired", b"payload-2", expired_lease),
    ]
    batch = database.batch.return_value.__enter__.return_value

    queue_receive_messages.receive_and_ack_queue_messages(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    database.batch.assert_called_once_with()
    batch.ack.assert_called_once_with(
        queue="UserTasks", key=[1, "msg-valid"], ignore_not_found=True
    )
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Acknowledged Messages: 1" in out
    assert "Queue Name: UserTasks" in out
    assert "Received Messages: 2" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("missing queue"),
            "error: queue 'UserTasks' on database",
        ),
        (
            exceptions.InvalidArgument("bad tvf"),
            "error: failed to receive or ack messages",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_receive_and_ack_queue_messages_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.side_effect = error

    queue_receive_messages.receive_and_ack_queue_messages(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_receive_and_ack_queue_messages_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "queue_receive_messages.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_queues.queue_receive_messages", run_name="__main__")

    assert "Received Messages: 0" in capsys.readouterr().out


@conftest.live_only
def test_receive_and_ack_queue_messages_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    queue_send_message.send_queue_message(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    capsys.readouterr()

    queue_receive_messages.receive_and_ack_queue_messages(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Queue Name: UserTasks" in out
    assert "Received Messages:" in out
