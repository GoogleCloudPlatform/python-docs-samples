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

import bigquery_query_biglake_gcs_temp_table
from google.api_core import exceptions
import pytest


def test_query_biglake_gcs_temp_table_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.job_id = "example-job-123"
    mock_job.result.return_value = [mock.MagicMock(), mock.MagicMock()]
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_query_biglake_gcs_temp_table.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_query_biglake_gcs_temp_table.query_biglake_gcs_temp_table(
        project_id="example-project",
        connection_id="projects/example-project/locations/us/connections/example-conn",
    )

    captured = capsys.readouterr()
    assert (
        "Resource ID: projects/example-project/locations/us/connections/example-conn"
        in captured.out
    )
    assert "Rows Returned: 2" in captured.out
    assert mock_client.query.called


def test_query_biglake_gcs_temp_table_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_job = mock.MagicMock()
    mock_job.result.side_effect = exceptions.NotFound("connection not found")
    mock_client.query.return_value = mock_job
    monkeypatch.setattr(
        bigquery_query_biglake_gcs_temp_table.bigquery,
        "Client",
        lambda project=None: mock_client,
    )

    bigquery_query_biglake_gcs_temp_table.query_biglake_gcs_temp_table(
        project_id="example-project",
        connection_id="projects/example-project/locations/us/connections/example-conn",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example-conn" in captured.err
