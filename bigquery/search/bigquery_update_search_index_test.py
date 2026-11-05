# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

import bigquery_update_search_index
from google.api_core import exceptions
import pytest


def test_update_search_index_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.job_id = "example-job-123"
    mock_job.statement_type = "ALTER_SEARCH_INDEX"
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_update_search_index.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_update_search_index.update_search_index(
        project_id="example-project",
        dataset_id="example_dataset",
        table_id="example_table",
    )

    captured = capsys.readouterr()
    assert "Resource ID: example-project.example_dataset.example_table" in captured.out
    assert "Index Name: example_search_index" in captured.out
    assert mock_client.query.called


def test_update_search_index_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.result.side_effect = exceptions.NotFound("index error")
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_update_search_index.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_update_search_index.update_search_index(
        project_id="example-project",
        dataset_id="example_dataset",
        table_id="example_table",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example_search_index" in captured.err
