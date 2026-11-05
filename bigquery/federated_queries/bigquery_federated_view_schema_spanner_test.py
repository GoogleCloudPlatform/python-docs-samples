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

import bigquery_federated_view_schema_spanner
from google.api_core import exceptions
import pytest


def test_federated_view_schema_spanner_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.job_id = "example-job-123"
    mock_job.result.return_value = [
        mock.MagicMock(),
        mock.MagicMock(),
        mock.MagicMock(),
    ]
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_federated_view_schema_spanner.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_federated_view_schema_spanner.federated_view_schema_spanner(
        project_id="example-project",
        connection_id="example-project.us.example-spanner-conn",
    )

    captured = capsys.readouterr()
    assert "Resource ID: example-project.us.example-spanner-conn" in captured.out
    assert "Columns Returned: 3" in captured.out
    assert mock_client.query.called


def test_federated_view_schema_spanner_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.result.side_effect = exceptions.NotFound("connection not found")
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_federated_view_schema_spanner.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_federated_view_schema_spanner.federated_view_schema_spanner(
        project_id="example-project",
        connection_id="example-project.us.example-spanner-conn",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example-spanner-conn" in captured.err
