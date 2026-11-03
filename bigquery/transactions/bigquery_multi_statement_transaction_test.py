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

import bigquery_multi_statement_transaction
from google.api_core import exceptions
import pytest


def test_run_multi_statement_transaction_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.job_id = "example-job-123"
        mock_job.num_child_jobs = 3
        mock_row = mock.MagicMock()
        mock_row.inventory_rows = 3
        mock_job.result.return_value = [mock_row]
        mock_client.query.return_value = mock_job

        bigquery_multi_statement_transaction.run_multi_statement_transaction(
            project_id="example-project",
            dataset_id="example_dataset",
            source_table_id="example_new_arrivals",
            target_table_id="example_inventory",
        )

        mock_client.query.assert_called_once()
        captured = capsys.readouterr()
        assert (
            "Resource ID: example-project.example_dataset.example_inventory"
            in captured.out
        )
        assert "Child Jobs: 3" in captured.out
        assert "Inventory Rows: 3" in captured.out
        assert "Transaction State: COMMITTED" in captured.out


def test_run_multi_statement_transaction_not_found(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.query.side_effect = exceptions.NotFound("Table not found")

        bigquery_multi_statement_transaction.run_multi_statement_transaction(
            project_id="example-project",
            dataset_id="example_dataset",
            source_table_id="example_new_arrivals",
            target_table_id="example_inventory",
        )

        captured = capsys.readouterr()
        assert "error:" in captured.err
        assert "example_inventory" in captured.err
