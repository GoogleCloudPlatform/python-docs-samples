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
from spanner_search_and_ai import create_embedding_model
from spanner_search_and_ai import ml_predict_embeddings

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_generate_and_query_embeddings_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [
        (3, "Cordless Drill", 0.184321),
        (2, "Mountain Bike", 0.612345),
    ]

    ml_predict_embeddings.generate_and_query_embeddings(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    sql = snapshot.execute_sql.call_args.args[0]
    assert "ML.PREDICT" in sql
    assert "MODEL TextEmbeddingModel" in sql
    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_NAME}" in out
    assert "Product ID: 3" in out
    assert "Product Name: Cordless Drill" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("missing db"),
            "error: database 'example-db' or model on instance",
        ),
        (
            exceptions.PermissionDenied("endpoint denied"),
            "error: ML.PREDICT embedding query failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_generate_and_query_embeddings_errors(
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

    ml_predict_embeddings.generate_and_query_embeddings(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith(expected_prefix)


@mock.patch(SPANNER_CLIENT)
def test_generate_and_query_embeddings_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(3, "Cordless Drill", 0.18)]
    monkeypatch.setattr(
        "sys.argv",
        [
            "ml_predict_embeddings.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_search_and_ai.ml_predict_embeddings", run_name="__main__")

    assert "Product Name: Cordless Drill" in capsys.readouterr().out


@conftest.live_only
def test_generate_and_query_embeddings_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    create_embedding_model.create_embedding_model(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_LOCATION_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    capsys.readouterr()

    ml_predict_embeddings.generate_and_query_embeddings(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Product Name: Cordless Drill" in out
