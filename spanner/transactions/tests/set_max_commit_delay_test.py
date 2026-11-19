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

import datetime
import runpy
from unittest import mock

from google.api_core import exceptions
from google.cloud import spanner
import pytest
from spanner_transactions import set_max_commit_delay

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


def _setup_txn(mock_client_class: mock.MagicMock) -> mock.MagicMock:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    txn = mock.MagicMock()
    database.run_in_transaction.side_effect = lambda fn, *a, **kw: fn(txn)
    return txn


@mock.patch(SPANNER_CLIENT)
def test_set_max_commit_delay_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    txn = _setup_txn(mock_client_class)
    txn.execute_update.return_value = 1

    set_max_commit_delay.set_max_commit_delay(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    assert database.run_in_transaction.call_args.kwargs["max_commit_delay"] == (
        datetime.timedelta(milliseconds=100)
    )
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Inserted Rows: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.AlreadyExists("dup"), "error: singer row already exists"),
        (
            exceptions.InvalidArgument("bad delay"),
            "error: max_commit_delay transaction failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_set_max_commit_delay_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    set_max_commit_delay.set_max_commit_delay(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_set_max_commit_delay_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    txn = _setup_txn(mock_client_class)
    txn.execute_update.return_value = 1
    monkeypatch.setattr(
        "sys.argv",
        [
            "set_max_commit_delay.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_transactions.set_max_commit_delay", run_name="__main__")

    assert "Inserted Rows: 1" in capsys.readouterr().out


@conftest.live_only
def test_set_max_commit_delay_live(capsys: pytest.CaptureFixture[str]) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    db = client.instance(conftest.LIVE_INSTANCE_ID).database(conftest.LIVE_DATABASE_ID)
    with db.batch() as batch:
        batch.delete("Singers", spanner.KeySet(keys=[[111]]))
    try:
        set_max_commit_delay.set_max_commit_delay(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Inserted Rows: 1" in out
    finally:
        with db.batch() as batch:
            batch.delete("Singers", spanner.KeySet(keys=[[111]]))
