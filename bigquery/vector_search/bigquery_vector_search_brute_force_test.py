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

import bigquery_vector_search_brute_force
from google.api_core import exceptions
import pytest


def test_vector_search_brute_force_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.job_id = "example-job-123"
        mock_job.result.return_value = [mock.MagicMock() for _ in range(5)]
        mock_client.query.return_value = mock_job

        bigquery_vector_search_brute_force.vector_search_brute_force(
            project_id="example-project",
        )

        mock_client.query.assert_called_once()
        captured = capsys.readouterr()
        assert "Resource ID: bigquery-public-data.bbc_news.fulltext" in captured.out
        assert "Embedding Dimensions: 768" in captured.out
        assert "Neighbors Returned: 5" in captured.out


def test_vector_search_brute_force_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.result.side_effect = exceptions.NotFound("Table not found")
        mock_client.query.return_value = mock_job

        bigquery_vector_search_brute_force.vector_search_brute_force(
            project_id="example-project",
        )

        captured = capsys.readouterr()
        assert "error:" in captured.err
        assert "bbc_news.fulltext" in captured.err
