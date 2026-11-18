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
from google.cloud import spanner
import pytest
from spanner_dml import dml_batch_update

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
    database.run_in_transaction.side_effect = lambda fn, *a, **kw: fn(txn, *a, **kw)
    return txn


@mock.patch(SPANNER_CLIENT)
def test_batch_update_dml_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    txn = _setup_txn(mock_client_class)
    status = mock.MagicMock(code=0)
    txn.batch_update.return_value = (status, [1, 1])

    dml_batch_update.batch_update_dml(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Executed Statements: 2" in out
    assert "Total Rows Modified: 2" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.AlreadyExists("dup"), "error: album row already exists"),
        (exceptions.PermissionDenied("denied"), "error: Batch DML failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_batch_update_dml_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    dml_batch_update.batch_update_dml(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_batch_update_dml_nonzero_status(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    txn = _setup_txn(mock_client_class)
    txn.batch_update.return_value = (mock.MagicMock(code=3, message="invalid"), [])

    dml_batch_update.batch_update_dml(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("error: Batch DML failed")
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_batch_update_dml_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    txn = _setup_txn(mock_client_class)
    txn.batch_update.return_value = (mock.MagicMock(code=0), [1, 1])
    monkeypatch.setattr(
        "sys.argv",
        [
            "dml_batch_update.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_dml.dml_batch_update", run_name="__main__")

    assert "Executed Statements: 2" in capsys.readouterr().out


@conftest.live_only
def test_batch_update_dml_live(capsys: pytest.CaptureFixture[str]) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    db = client.instance(conftest.LIVE_INSTANCE_ID).database(conftest.LIVE_DATABASE_ID)
    with db.batch() as batch:
        batch.delete("Albums", spanner.KeySet(keys=[[1, 3]]))
    try:
        dml_batch_update.batch_update_dml(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Executed Statements: 2" in out
        assert "Total Rows Modified: 2" in out
    finally:
        with db.batch() as batch:
            batch.delete("Albums", spanner.KeySet(keys=[[1, 3]]))
