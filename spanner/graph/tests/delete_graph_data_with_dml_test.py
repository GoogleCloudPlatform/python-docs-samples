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
from spanner_graph import delete_graph_data_with_dml
from spanner_graph import insert_graph_data_with_dml

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
def test_delete_graph_data_with_dml_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    txn = _setup_txn(mock_client_class)
    txn.execute_update.side_effect = [1, 1]

    delete_graph_data_with_dml.delete_graph_data_with_dml(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Deleted Accounts: 1" in out
    assert "Deleted Transfers: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.FailedPrecondition("fk"),
            "error: foreign-key constraint blocked graph delete",
        ),
        (exceptions.PermissionDenied("denied"), "error: graph DML delete failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_delete_graph_data_with_dml_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.run_in_transaction.side_effect = error

    delete_graph_data_with_dml.delete_graph_data_with_dml(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_delete_graph_data_with_dml_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    txn = _setup_txn(mock_client_class)
    txn.execute_update.side_effect = [1, 1]
    monkeypatch.setattr(
        "sys.argv",
        [
            "delete_graph_data_with_dml.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_graph.delete_graph_data_with_dml", run_name="__main__")

    assert "Deleted Accounts: 1" in capsys.readouterr().out


@conftest.live_only
def test_delete_graph_data_with_dml_live(capsys: pytest.CaptureFixture[str]) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    db = client.instance(conftest.LIVE_INSTANCE_ID).database(conftest.LIVE_DATABASE_ID)
    db.execute_partitioned_dml("DELETE FROM Account WHERE id IN (1, 2)")
    try:
        insert_graph_data_with_dml.insert_graph_data_with_dml(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        capsys.readouterr()
        delete_graph_data_with_dml.delete_graph_data_with_dml(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Deleted Accounts: 1" in out
        assert "Deleted Transfers: 1" in out
    finally:
        db.execute_partitioned_dml("DELETE FROM Account WHERE id IN (1, 2)")
