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

import bigquery_read_biglake_gcs_storage_api
from google.api_core import exceptions
import pytest


def test_read_biglake_gcs_storage_api_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_session = mock.MagicMock()
    mock_session.name = "projects/example-project/locations/us/sessions/s1"
    mock_stream = mock.MagicMock()
    mock_stream.name = "projects/example-project/locations/us/sessions/s1/streams/0"
    mock_session.streams = [mock_stream]
    mock_client.create_read_session.return_value = mock_session

    mock_response = mock.MagicMock()
    mock_response.row_count = 3
    mock_client.read_rows.return_value = [mock_response]

    monkeypatch.setattr(
        bigquery_read_biglake_gcs_storage_api.bigquery_storage_v1,
        "BigQueryReadClient",
        lambda: mock_client,
    )

    bigquery_read_biglake_gcs_storage_api.read_biglake_gcs_storage_api(
        project_id="example-project",
        dataset_id="example_dataset",
        table_id="example_biglake_table",
    )

    captured = capsys.readouterr()
    assert (
        "Resource ID: projects/example-project/datasets/example_dataset/tables/example_biglake_table"
        in captured.out
    )
    assert "Rows Read: 3" in captured.out
    assert "Stream Count: 1" in captured.out


def test_read_biglake_gcs_storage_api_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_client.create_read_session.side_effect = exceptions.NotFound("table not found")
    monkeypatch.setattr(
        bigquery_read_biglake_gcs_storage_api.bigquery_storage_v1,
        "BigQueryReadClient",
        lambda: mock_client,
    )

    bigquery_read_biglake_gcs_storage_api.read_biglake_gcs_storage_api(
        project_id="example-project",
        dataset_id="example_dataset",
        table_id="example_biglake_table",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example_biglake_table" in captured.err
