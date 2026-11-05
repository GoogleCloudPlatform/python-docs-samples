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

import bigquery_get_vector_index_status
from google.api_core import exceptions
import pytest


def test_get_vector_index_status_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.job_id = "example-job-123"
        mock_row = mock.MagicMock()
        mock_row.index_name = "example_vector_index"
        mock_row.index_status = "ACTIVE"
        mock_row.coverage_percentage = 100
        mock_job.result.return_value = [mock_row]
        mock_client.query.return_value = mock_job

        bigquery_get_vector_index_status.get_vector_index_status(
            project_id="example-project",
            dataset_id="example_dataset",
            table_id="example_embeddings",
        )

        mock_client.query.assert_called_once()
        captured = capsys.readouterr()
        assert (
            "Resource ID: example-project.example_dataset.example_embeddings"
            in captured.out
        )
        assert "Index Count: 1" in captured.out
        assert "Index Name: example_vector_index" in captured.out
        assert "Index Status: ACTIVE" in captured.out
        assert "Coverage Percentage: 100%" in captured.out


def test_get_vector_index_status_not_found(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.result.side_effect = exceptions.NotFound("Dataset not found")
        mock_client.query.return_value = mock_job

        bigquery_get_vector_index_status.get_vector_index_status(
            project_id="example-project",
            dataset_id="example_dataset",
            table_id="example_embeddings",
        )

        captured = capsys.readouterr()
        assert "error:" in captured.err
        assert "example_embeddings" in captured.err
