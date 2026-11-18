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
from spanner_dml import dml_partitioned_delete

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_delete_data_with_partitioned_dml_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.execute_partitioned_dml.return_value = 2

    dml_partitioned_delete.delete_data_with_partitioned_dml(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert "Deleted Lower Bound: 2" in out
    assert PROJECT_ID not in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (exceptions.NotFound("missing"), "error: database 'example-db'"),
        (
            exceptions.InvalidArgument("non-partitionable"),
            "error: Partitioned DML delete failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_delete_data_with_partitioned_dml_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.execute_partitioned_dml.side_effect = error

    dml_partitioned_delete.delete_data_with_partitioned_dml(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_delete_data_with_partitioned_dml_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.execute_partitioned_dml.return_value = 2
    monkeypatch.setattr(
        "sys.argv",
        [
            "dml_partitioned_delete.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_dml.dml_partitioned_delete", run_name="__main__")

    assert "Deleted Lower Bound: 2" in capsys.readouterr().out


@conftest.live_only
def test_delete_data_with_partitioned_dml_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = spanner.Client(project=conftest.LIVE_PROJECT_ID)
    db = client.instance(conftest.LIVE_INSTANCE_ID).database(conftest.LIVE_DATABASE_ID)
    with db.snapshot(multi_use=True) as snap:
        saved_singers = list(
            snap.execute_sql(
                "SELECT SingerId, FirstName, LastName FROM Singers WHERE SingerId > 10"
            )
        )
        saved_albums = list(
            snap.execute_sql(
                "SELECT SingerId, AlbumId, AlbumTitle, MarketingBudget "
                "FROM Albums WHERE SingerId > 10"
            )
        )
    with db.batch() as batch:
        batch.insert_or_update(
            table="Singers",
            columns=("SingerId", "FirstName", "LastName"),
            values=[(19, "Temp", "DeleteCandidate")],
        )
    try:
        dml_partitioned_delete.delete_data_with_partitioned_dml(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert conftest.LIVE_PROJECT_ID not in out
        assert "Deleted Lower Bound:" in out
    finally:
        if saved_singers:
            with db.batch() as batch:
                batch.insert_or_update(
                    table="Singers",
                    columns=("SingerId", "FirstName", "LastName"),
                    values=saved_singers,
                )
                if saved_albums:
                    batch.insert_or_update(
                        table="Albums",
                        columns=(
                            "SingerId",
                            "AlbumId",
                            "AlbumTitle",
                            "MarketingBudget",
                        ),
                        values=saved_albums,
                    )
