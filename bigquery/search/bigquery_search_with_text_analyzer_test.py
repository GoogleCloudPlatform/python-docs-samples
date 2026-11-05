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

import bigquery_search_with_text_analyzer
from google.api_core import exceptions
import pytest


def test_search_with_text_analyzer_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.job_id = "example-job-123"
    mock_job.result.return_value = []
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_search_with_text_analyzer.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_search_with_text_analyzer.search_with_text_analyzer(
        project_id="example-project",
    )

    captured = capsys.readouterr()
    assert "Resource ID: bigquery-public-data.thelook_ecommerce.users" in captured.out
    assert "Analyzer: NO_OP_ANALYZER" in captured.out
    assert mock_client.query.called


def test_search_with_text_analyzer_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.result.side_effect = exceptions.NotFound("resource error")
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_search_with_text_analyzer.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_search_with_text_analyzer.search_with_text_analyzer(
        project_id="example-project",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example-project" in captured.err
