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

import uuid

import google.cloud.dlp_v2

import inspect_gcs_send_to_scc as inspect_content

import pytest

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources")


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_gcs_send_to_scc(
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

    file = open(os.path.join(RESOURCE_DIRECTORY, "test.txt"), "r")
    # read the content of file
    data = file.read()
    # get the length of the data
    number_of_characters = len(data)

    mock_job.inspect_details.result.processed_bytes = number_of_characters
    mock_job.inspect_details.result.info_type_stats.info_type.name = "EMAIL_ADDRESS"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the sample.
    inspect_content.inspect_gcs_send_to_scc(
        GCLOUD_PROJECT,
        f"{TEST_BUCKET_NAME}//test.txt",
        ["EMAIL_ADDRESS"],
        100,
    )

    out, _ = capsys.readouterr()
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()
