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
import pytest
from spanner_googlesql import data_boost_partitioned_query

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_run_data_boost_partitioned_query_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.batch_snapshot.return_value
    snapshot.generate_query_batches.return_value = ["part-1", "part-2"]
    snapshot.process_query_batch.side_effect = [
        [(1, "Marc", "Richards"), (2, "Catalina", "Smith")],
        [(3, "Alice", "Trentor")],
    ]

    data_boost_partitioned_query.run_data_boost_partitioned_query(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    snapshot.generate_query_batches.assert_called_once_with(
        sql="SELECT SingerId, FirstName, LastName FROM Singers",
        data_boost_enabled=True,
    )
    snapshot.close.assert_called_once()
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_NAME}" in out
    assert "Partition Count: 2" in out
    assert "Total Rows: 3" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.PermissionDenied("missing useDataBoost"),
            "error: Data Boost partitioned query failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_run_data_boost_partitioned_query_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.batch_snapshot.return_value
    snapshot.generate_query_batches.side_effect = error

    data_boost_partitioned_query.run_data_boost_partitioned_query(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    snapshot.close.assert_called_once()
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)


@mock.patch(SPANNER_CLIENT)
def test_run_data_boost_partitioned_query_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.batch_snapshot.return_value
    snapshot.generate_query_batches.return_value = ["part-1"]
    snapshot.process_query_batch.return_value = [(1, "Marc", "Richards")]
    monkeypatch.setattr(
        "sys.argv",
        [
            "data_boost_partitioned_query.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_googlesql.data_boost_partitioned_query", run_name="__main__"
    )

    assert "Total Rows: 1" in capsys.readouterr().out


@conftest.live_only
def test_run_data_boost_partitioned_query_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    data_boost_partitioned_query.run_data_boost_partitioned_query(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Partition Count:" in out
    assert "Total Rows: 3" in out
