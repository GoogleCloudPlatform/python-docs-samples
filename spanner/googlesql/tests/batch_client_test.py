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
from spanner_googlesql import batch_client

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_run_batch_read_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.batch_snapshot.return_value
    snapshot.generate_read_batches.return_value = [{"p": 1}, {"p": 2}]
    snapshot.process_read_batch.side_effect = [
        [(1, "Marc", "Richards")],
        [(2, "Catalina", "Smith")],
    ]

    batch_client.run_batch_read(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    assert snapshot.generate_read_batches.call_args.kwargs["data_boost_enabled"] is True
    snapshot.close.assert_called_once_with()
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Partition Count: 2" in out
    assert "Total Rows: 2" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: table or database 'example-db'"),
        (
            exceptions.PermissionDenied("denied"),
            "error: partitioned batch read failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_run_batch_read_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.batch_snapshot.return_value.generate_read_batches.side_effect = error

    batch_client.run_batch_read(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_run_batch_read_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.batch_snapshot.return_value
    snapshot.generate_read_batches.return_value = [{"p": 1}]
    snapshot.process_read_batch.return_value = [(1, "Marc", "Richards")]
    monkeypatch.setattr(
        "sys.argv",
        [
            "batch_client.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_googlesql.batch_client", run_name="__main__")

    assert "Total Rows: 1" in capsys.readouterr().out


@conftest.live_only
def test_run_batch_read_live(capsys: pytest.CaptureFixture[str]) -> None:
    batch_client.run_batch_read(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Partition Count:" in out
    row_lines = [ln for ln in out.splitlines() if ln.startswith("Total Rows: ")]
    assert len(row_lines) == 1
    assert int(row_lines[0].split(": ", 1)[1]) >= 3
