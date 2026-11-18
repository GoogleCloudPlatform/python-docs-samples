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
from spanner_dml import batch_write_at_least_once

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_batch_write_at_least_once_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    groups = database.mutation_groups.return_value.__enter__.return_value
    resp = mock.MagicMock()
    resp.indexes = [0, 1]
    resp.status.code = 0
    resp.commit_timestamp = "2026-01-15T12:00:00Z"
    groups.batch_write.return_value = [resp]

    batch_write_at_least_once.batch_write_at_least_once(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Applied Group Indexes: [0, 1]" in out
    assert "Total Groups Processed: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: database 'example-db'"),
        (exceptions.PermissionDenied("denied"), "error: BatchWrite RPC failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_batch_write_at_least_once_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.mutation_groups.return_value.__enter__.side_effect = error

    batch_write_at_least_once.batch_write_at_least_once(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_batch_write_at_least_once_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    groups = database.mutation_groups.return_value.__enter__.return_value
    resp = mock.MagicMock(indexes=[0, 1], commit_timestamp="2026-01-15T12:00:00Z")
    resp.status.code = 0
    groups.batch_write.return_value = [resp]
    monkeypatch.setattr(
        "sys.argv",
        [
            "batch_write_at_least_once.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_dml.batch_write_at_least_once", run_name="__main__")

    assert "Total Groups Processed: 1" in capsys.readouterr().out


@conftest.live_only
def test_batch_write_at_least_once_live(capsys: pytest.CaptureFixture[str]) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    db = client.instance(conftest.LIVE_INSTANCE_ID).database(conftest.LIVE_DATABASE_ID)
    try:
        batch_write_at_least_once.batch_write_at_least_once(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Applied Group Indexes:" in out
    finally:
        with db.batch() as batch:
            batch.delete("Albums", spanner.KeySet(keys=[[17, 1], [18, 2]]))
            batch.delete("Singers", spanner.KeySet(keys=[[16], [17], [18]]))
