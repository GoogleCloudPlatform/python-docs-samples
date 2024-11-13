# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from unittest import mock
from unittest.mock import MagicMock

import google.cloud.dlp_v2

import inspect_bigquery_send_to_scc as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_bigquery_send_to_scc(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = (
        f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    )

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"

    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    mock_job.inspect_details.result.info_type_stats.info_type.name = "PERSON_NAME"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the sample.
    inspect_content.inspect_bigquery_send_to_scc(
        GCLOUD_PROJECT,
        ["PERSON_NAME"],
    )

    out, _ = capsys.readouterr()
    assert "Info type: PERSON_NAME" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()
