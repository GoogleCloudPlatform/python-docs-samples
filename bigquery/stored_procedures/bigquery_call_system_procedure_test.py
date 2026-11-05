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

import bigquery_call_system_procedure
from google.api_core import exceptions
import pytest


def test_call_system_procedure_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.job_id = "example-job-123"
        mock_job.statement_type = "SCRIPT"
        mock_job.result.return_value = []
        mock_client.query.return_value = mock_job

        bigquery_call_system_procedure.call_system_procedure(
            project_id="example-project",
            dataset_id="example_dataset",
            materialized_view_id="example_mv",
        )

        mock_client.query.assert_called_once()
        captured = capsys.readouterr()
        assert "Resource ID: example-project.example_dataset.example_mv" in captured.out
        assert "Statement Type: SCRIPT" in captured.out
        assert "System Procedure: BQ.REFRESH_MATERIALIZED_VIEW" in captured.out


def test_call_system_procedure_not_found(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.result.side_effect = exceptions.NotFound("View not found")
        mock_client.query.return_value = mock_job

        bigquery_call_system_procedure.call_system_procedure(
            project_id="example-project",
            dataset_id="example_dataset",
            materialized_view_id="example_mv",
        )

        captured = capsys.readouterr()
        assert "error:" in captured.err
        assert "example_mv" in captured.err
