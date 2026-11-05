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

import bigquery_call_procedure
from google.api_core import exceptions
import pytest


def test_call_procedure_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.job_id = "example-job-123"
    mock_row = mock.MagicMock()
    mock_row.total_words = 42
    mock_job.result.return_value = [mock_row]
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_call_procedure.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_call_procedure.call_procedure(
        project_id="example-project",
        dataset_id="example_dataset",
        procedure_id="example_procedure",
    )

    captured = capsys.readouterr()
    assert "Resource ID:" in captured.out
    assert "example-project" in captured.out
    assert mock_client.query.called


def test_call_procedure_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_client.query.side_effect = exceptions.NotFound("resource error")
    monkeypatch.setattr(
        bigquery_call_procedure.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_call_procedure.call_procedure(
        project_id="example-project",
        dataset_id="example_dataset",
        procedure_id="example_procedure",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example-project" in captured.err
