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
from google.cloud import spanner_admin_database_v1
import pytest
from spanner_search_and_ai import create_vector_index

from . import conftest

PROJECT_ID = "example-project-id"
INSTANCE_ID = "example-instance"
DATABASE_ID = "example-db"
DATABASE_PATH = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}/databases/{DATABASE_ID}"
ADMIN_CLIENT = "google.cloud.spanner_admin_database_v1.DatabaseAdminClient"


@mock.patch(ADMIN_CLIENT)
def test_create_vector_index_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH

    create_vector_index.create_vector_index(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    request = client.update_database_ddl.call_args.kwargs["request"]
    assert request.database == DATABASE_PATH
    assert "CREATE VECTOR INDEX DocEmbeddingIndex" in request.statements[0]
    assert "WHERE DocEmbedding IS NOT NULL" in request.statements[0]
    client.update_database_ddl.return_value.result.assert_called_once_with(timeout=300)

    out, err = capsys.readouterr()
    assert "Waiting for vector index 'DocEmbeddingIndex'" in out
    assert f"Resource ID: {DATABASE_ID}" in out
    assert PROJECT_ID not in out
    assert "Index Name: DocEmbeddingIndex" in out
    assert err == ""


@pytest.mark.parametrize(
    "error, expected_prefix",
    [
        (
            exceptions.FailedPrecondition("Duplicate name"),
            "error: vector index 'DocEmbeddingIndex' already exists",
        ),
        (
            exceptions.PermissionDenied("denied"),
            "error: failed to create vector index 'DocEmbeddingIndex'",
        ),
    ],
)
@mock.patch(ADMIN_CLIENT)
def test_create_vector_index_errors(
    mock_client_class: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    expected_prefix: str,
) -> None:
    client = mock_client_class.return_value
    client.database_path.return_value = DATABASE_PATH
    client.update_database_ddl.side_effect = error

    create_vector_index.create_vector_index(PROJECT_ID, INSTANCE_ID, DATABASE_ID)

    _out, err = capsys.readouterr()
    assert err.startswith(expected_prefix)
    assert PROJECT_ID not in err
    assert PROJECT_ID not in err


@mock.patch(ADMIN_CLIENT)
def test_create_vector_index_cli_entrypoint(
    mock_client_class: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client_class.return_value.database_path.return_value = DATABASE_PATH
    monkeypatch.setattr(
        "sys.argv",
        [
            "create_vector_index.py",
            "--project-id",
            PROJECT_ID,
            "--instance-id",
            INSTANCE_ID,
            "--database-id",
            DATABASE_ID,
        ],
    )

    runpy.run_module("spanner_search_and_ai.create_vector_index", run_name="__main__")

    assert "Index Name: DocEmbeddingIndex" in capsys.readouterr().out


@conftest.live_only
def test_create_vector_index_live(
    capsys: pytest.CaptureFixture[str],
) -> None:
    admin_client = spanner_admin_database_v1.DatabaseAdminClient()
    db_path = admin_client.database_path(
        conftest.LIVE_PROJECT_ID,
        conftest.LIVE_INSTANCE_ID,
        conftest.LIVE_DATABASE_ID,
    )
    admin_client.update_database_ddl(
        request=spanner_admin_database_v1.UpdateDatabaseDdlRequest(
            database=db_path,
            statements=["DROP VECTOR INDEX IF EXISTS DocEmbeddingIndex"],
        )
    ).result(timeout=300)

    try:
        create_vector_index.create_vector_index(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        out, err = capsys.readouterr()
        assert err == ""
        assert "Index Name: DocEmbeddingIndex" in out

        # Duplicate creation exercises the FailedPrecondition error arm cleanly.
        create_vector_index.create_vector_index(
            conftest.LIVE_PROJECT_ID,
            conftest.LIVE_INSTANCE_ID,
            conftest.LIVE_DATABASE_ID,
        )
        _dup_out, dup_err = capsys.readouterr()
        assert dup_err.startswith(
            "error: vector index 'DocEmbeddingIndex' already exists"
        )
    finally:
        admin_client.update_database_ddl(
            request=spanner_admin_database_v1.UpdateDatabaseDdlRequest(
                database=db_path,
                statements=["DROP VECTOR INDEX IF EXISTS DocEmbeddingIndex"],
            )
        ).result(timeout=300)
