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

import bigquery_upgrade_manifest_biglake_table
from google.api_core import exceptions
import pytest


def test_upgrade_manifest_biglake_table_success(
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

        bigquery_upgrade_manifest_biglake_table.upgrade_manifest_biglake_table(
            project_id="example-project",
            dataset_id="example_dataset",
            table_id="example_manifest_table",
            connection_id="example-project.us.example_biglake_conn",
            manifest_uri="gs://example-bucket/manifests/symlink.manifest",
        )

        mock_client.query.assert_called_once()
        captured = capsys.readouterr()
        assert (
            "Resource ID: example-project.example_dataset.example_manifest_table"
            in captured.out
        )
        assert "Metadata Cache Mode: AUTOMATIC" in captured.out
        assert "Rows Returned: 3" in captured.out


def test_upgrade_manifest_biglake_table_not_found(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with mock.patch("google.cloud.bigquery.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_job = mock.MagicMock()
        mock_job.result.side_effect = exceptions.NotFound("Connection not found")
        mock_client.query.return_value = mock_job

        bigquery_upgrade_manifest_biglake_table.upgrade_manifest_biglake_table(
            project_id="example-project",
            dataset_id="example_dataset",
            table_id="example_manifest_table",
            connection_id="example-project.us.example_biglake_conn",
            manifest_uri="gs://example-bucket/manifests/symlink.manifest",
        )

        captured = capsys.readouterr()
        assert "error:" in captured.err
        assert "example_manifest_table" in captured.err
