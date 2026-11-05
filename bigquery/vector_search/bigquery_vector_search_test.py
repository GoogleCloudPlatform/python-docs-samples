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

import bigquery_vector_search
from google.api_core import exceptions
import pytest


def test_vector_search_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.job_id = "example-job-123"
        mock_job.result.return_value = [
            mock.MagicMock(),
            mock.MagicMock(),
            mock.MagicMock(),
        ]
        mock_client.query.return_value = mock_job

        bigquery_vector_search.vector_search(
            project_id="example-project",
            dataset_id="example_dataset",
            table_id="example_embeddings",
        )

        mock_client.query.assert_called_once()
        sql_called = mock_client.query.call_args[0][0]
        assert "fraction_lists_to_search" in sql_called
        captured = capsys.readouterr()
        assert (
            "Resource ID: example-project.example_dataset.example_embeddings"
            in captured.out
        )
        assert "Embedding Dimensions: 4" in captured.out
        assert "Neighbors Returned: 3" in captured.out


def test_vector_search_not_found(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.result.side_effect = exceptions.NotFound("Table not found")
        mock_client.query.return_value = mock_job

        bigquery_vector_search.vector_search(
            project_id="example-project",
            dataset_id="example_dataset",
            table_id="example_embeddings",
        )

        captured = capsys.readouterr()
        assert "error:" in captured.err
        assert "example_embeddings" in captured.err
