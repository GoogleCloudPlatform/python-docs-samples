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

import dataplex_get_data_profile_scan
from google.api_core import exceptions
import pytest


def test_get_data_profile_scan_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_scan = mock.MagicMock()
    mock_scan.name = (
        "projects/example-project/locations/us-central1/dataScans/example-profile-scan"
    )
    mock_scan.data.resource = "//bigquery.googleapis.com/projects/bigquery-public-data/datasets/samples/tables/shakespeare"
    mock_scan.data_profile_result.row_count = 164656
    mock_scan.state.name = "ACTIVE"
    mock_client.get_data_scan.return_value = mock_scan
    monkeypatch.setattr(
        dataplex_get_data_profile_scan.dataplex_v1,
        "DataScanServiceClient",
        lambda: mock_client,
    )

    dataplex_get_data_profile_scan.get_data_profile_scan(
        project_id="example-project",
        location="us-central1",
        data_scan_id="example-profile-scan",
    )

    captured = capsys.readouterr()
    assert (
        "Resource ID: projects/example-project/locations/us-central1/dataScans/example-profile-scan"
        in captured.out
    )
    assert "Row Count: 164656" in captured.out
    assert "Scan State: ACTIVE" in captured.out


def test_get_data_profile_scan_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_client = mock.MagicMock()
    mock_client.get_data_scan.side_effect = exceptions.NotFound("scan not found")
    monkeypatch.setattr(
        dataplex_get_data_profile_scan.dataplex_v1,
        "DataScanServiceClient",
        lambda: mock_client,
    )

    dataplex_get_data_profile_scan.get_data_profile_scan(
        project_id="example-project",
        location="us-central1",
        data_scan_id="example-profile-scan",
    )

    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "example-profile-scan" in captured.err
