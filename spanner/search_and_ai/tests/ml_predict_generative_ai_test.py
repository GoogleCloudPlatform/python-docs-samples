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
from spanner_search_and_ai import ml_predict_generative_ai

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_NAME = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
SPANNER_CLIENT = "google.cloud.spanner.Client"


@mock.patch(SPANNER_CLIENT)
def test_generate_product_recommendations_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [
        (1, "Plush Bear", "NO"),
        (2, "Mountain Bike", "NO"),
        (3, "Cordless Drill", "YES"),
    ]

    ml_predict_generative_ai.generate_product_recommendations(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    ddl_args = database.update_ddl.call_args.args[0]
    assert "CREATE MODEL IF NOT EXISTS GeminiRecommendationModel" in ddl_args[0]
    assert "locations/global/publishers/google/models/gemini-3.8-flash" in ddl_args[0]
    database.update_ddl.return_value.result.assert_called_once_with(timeout=300)

    out, err = capsys.readouterr()
    assert f"Resource ID: {DATABASE_NAME}" in out
    assert "Product Name: Cordless Drill" in out
    assert "RECOMMENDATION: YES" in out.upper()
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.NotFound("model not found"),
            "error: database 'example-db' or Vertex AI model",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: Gemini ML.PREDICT recommendation query failed",
        ),
    ],
)
@mock.patch(SPANNER_CLIENT)
def test_generate_product_recommendations_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.update_ddl.side_effect = error

    ml_predict_generative_ai.generate_product_recommendations(
        PROJECT_ID, INSTANCE_ID, DATABASE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)


@mock.patch(SPANNER_CLIENT)
def test_generate_product_recommendations_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    database = (
        mock_client_class.return_value.instance.return_value.database.return_value
    )
    database.name = DATABASE_NAME
    snapshot = database.snapshot.return_value.__enter__.return_value
    snapshot.execute_sql.return_value = [(3, "Cordless Drill", "YES")]
    monkeypatch.setattr(
        "sys.argv",
        [
            "ml_predict_generative_ai.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_search_and_ai.ml_predict_generative_ai", run_name="__main__"
    )

    assert "Recommendation: YES" in capsys.readouterr().out


@conftest.live_only
def test_generate_product_recommendations_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    ml_predict_generative_ai.generate_product_recommendations(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Product Name: Cordless Drill" in out
    assert "RECOMMENDATION: YES" in out.upper()
