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

from collections.abc import Callable
import runpy
from unittest import mock

from google.api_core import exceptions
from google.cloud import spanner
from google.cloud.spanner_v1 import KeySet
import pytest
from spanner_change_streams import set_exclude_txn_from_change_streams

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_set_exclude_txn_from_change_streams_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_update.side_effect = [1, 1]

    def run_txn(
        fn: Callable[[mock.MagicMock], None],
        exclude_txn_from_change_streams: bool = False,
    ) -> None:
        assert exclude_txn_from_change_streams is True
        fn(transaction)

    database.run_in_transaction.side_effect = run_txn

    set_exclude_txn_from_change_streams.set_exclude_txn_from_change_streams(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Excluded From Change Streams: True" in out
    assert "Modified Statements: 2" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.Aborted("aborted"),
            "error: change-stream excluded transaction failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_set_exclude_txn_from_change_streams_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    set_exclude_txn_from_change_streams.set_exclude_txn_from_change_streams(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_set_exclude_txn_from_change_streams_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    transaction = mock.MagicMock()
    transaction.execute_update.side_effect = [1, 1]
    database.run_in_transaction.side_effect = lambda fn, **_kw: fn(transaction)
    monkeypatch.setattr(
        "sys.argv",
        [
            "set_exclude_txn_from_change_streams.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_change_streams.set_exclude_txn_from_change_streams",
        run_name="__main__",
    )

    assert "Excluded From Change Streams: True" in capsys.readouterr().out


@conftest.live_only
def test_set_exclude_txn_from_change_streams_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    database = client.instance(conftest.LIVE_INSTANCE_ID).database(
        conftest.LIVE_DATABASE_ID
    )
    try:
        set_exclude_txn_from_change_streams.set_exclude_txn_from_change_streams(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert "Excluded From Change Streams: True" in out
    finally:
        with database.batch() as batch:
            batch.delete(table="Singers", keyset=KeySet(keys=[[101]]))
