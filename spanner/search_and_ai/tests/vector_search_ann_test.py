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
from spanner_search_and_ai import vector_search_ann

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_find_approximate_nearest_neighbors_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [
        (1, "Ultralight Alpine Tent", 0.001234),
        (2, "Backcountry Down Sleeping Bag", 0.003456),
    ]

    vector_search_ann.find_approximate_nearest_neighbors(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    sql = snapshot.execute_sql.call_args.args[0]
    assert "APPROX_COSINE_DISTANCE" in sql
    assert "FORCE_INDEX=CatalogEmbeddingIndex" in sql
    assert "Embedding IS NOT NULL" in sql
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Item ID: 1" in out
    assert "Title: Ultralight Alpine Tent" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("db missing"),
            "error: database 'example-db' on instance 'example-instance'",
        ),
        (
            exceptions.InvalidArgument("missing index"),
            "error: ANN vector search failed on database 'example-db'",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_find_approximate_nearest_neighbors_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.side_effect = error

    vector_search_ann.find_approximate_nearest_neighbors(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(SPANNER_CLIENT)
def test_find_approximate_nearest_neighbors_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(1, "Ultralight Alpine Tent", 0.001)]
    monkeypatch.setattr(
        "sys.argv",
        [
            "vector_search_ann.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_search_and_ai.vector_search_ann", run_name="__main__")

    assert "Item ID: 1" in capsys.readouterr().out


@conftest.live_only
def test_find_approximate_nearest_neighbors_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    vector_search_ann.find_approximate_nearest_neighbors(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Item ID: 1" in out
    assert "Title: Ultralight Alpine Tent" in out
