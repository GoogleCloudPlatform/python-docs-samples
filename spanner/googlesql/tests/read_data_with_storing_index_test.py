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
from spanner_googlesql import read_data_with_storing_index

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_read_data_with_storing_index_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.read.return_value = [(1, "Total Junk", 100000)]

    read_data_with_storing_index.read_data_with_storing_index(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    assert snapshot.read.call_args.kwargs["index"] == "AlbumsByAlbumTitle2"
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Album ID: 1, Title: Total Junk, Budget: 100000" in out
    assert "Row Count: 1" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: index 'AlbumsByAlbumTitle2'"),
        (exceptions.InvalidArgument("bad col"), "error: storing-index read failed"),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_read_data_with_storing_index_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.snapshot.return_value.__enter__.return_value.read.side_effect = error

    read_data_with_storing_index.read_data_with_storing_index(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_read_data_with_storing_index_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.snapshot.return_value.__enter__.return_value.read.return_value = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "read_data_with_storing_index.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_googlesql.read_data_with_storing_index", run_name="__main__"
    )

    assert "Row Count: 0" in capsys.readouterr().out


@conftest.live_only
def test_read_data_with_storing_index_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    read_data_with_storing_index.read_data_with_storing_index(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert conftest.LIVE_PROJECT_ID not in out
    assert "Title: Total Junk" in out
