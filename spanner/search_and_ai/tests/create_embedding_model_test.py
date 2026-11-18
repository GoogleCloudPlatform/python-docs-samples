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

from . import conftest

PROJECT_ID = "example-project-id"
LOCATION_ID = "us-central1"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_PATH = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_embedding_model_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH

    create_embedding_model.create_embedding_model(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID, DATABASE_ID
    )

    request = client.update_database_ddl.call_args.kwargs["request"]
    assert "CREATE OR REPLACE MODEL TextEmbeddingModel" in request.statements[0]
    assert "publishers/google/models/text-embedding-005" in request.statements[0]
    client.update_database_ddl.return_value.result.assert_called_once_with(timeout=300)

    out, err = capsys.readouterr()
    assert "Waiting for remote model 'TextEmbeddingModel'" in out
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Model Name: TextEmbeddingModel" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (TimeoutError("deadline"), "error: timed out waiting for the operation"),
        (
            exceptions.AlreadyExists("model exists"),
            "error: model 'TextEmbeddingModel' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to register model 'TextEmbeddingModel'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_embedding_model_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH
    client.update_database_ddl.side_effect = error

    create_embedding_model.create_embedding_model(
        PROJECT_ID, LOCATION_ID, INSTANCE_ID, DATABASE_ID
    )

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_embedding_model_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.database_path.return_value = DATABASE_PATH
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_embedding_model.py",
            "--project-id",
            PROJECT_ID,
            "--location-id",
            LOCATION_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module(
        "spanner_search_and_ai.create_embedding_model", run_name="__main__"
    )

    assert "Model Name: TextEmbeddingModel" in capsys.readouterr().out


@conftest.live_only
def test_create_embedding_model_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    create_embedding_model.create_embedding_model(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_LOCATION_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )

    out, err = capsys.readouterr()
    assert err == ""
    assert "Model Name: TextEmbeddingModel" in out
