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
from spanner_googlesql import insert_data_with_timestamp_column

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_insert_data_with_timestamp_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    batch = database.batch.return_value.__enter__.return_value

    insert_data_with_timestamp_column.insert_data_with_timestamp(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    batch.insert.assert_called_once()
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Inserted Performances: 3" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.AlreadyExists("dup"),
            "error: one or more Performances rows already exist",
        ),
        (
            exceptions.NotFound("missing"),
            "error: COMMIT_TIMESTAMP insert failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_insert_data_with_timestamp_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.batch.return_value.__exit__.side_effect = error

    insert_data_with_timestamp_column.insert_data_with_timestamp(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_insert_data_with_timestamp_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "insert_data_with_timestamp_column.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_googlesql.insert_data_with_timestamp_column", run_name="__main__"
    )

    assert "Inserted Performances: 3" in capsys.readouterr().out


@conftest.live_only
def test_insert_data_with_timestamp_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    database = client.instance(conftest.LIVE_INSTANCE_ID).database(
        conftest.LIVE_DATABASE_ID
    )
    keys = spanner.KeySet(
        keys=[
            [1, 4, "2017-10-05"],
            [1, 19, "2017-11-02"],
            [2, 42, "2017-12-23"],
        ]
    )
    with database.batch() as batch:
        batch.delete("Performances", keys)
    try:
        insert_data_with_timestamp_column.insert_data_with_timestamp(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Inserted Performances: 3" in out
    finally:
        with database.batch() as batch:
            batch.delete("Performances", keys)
