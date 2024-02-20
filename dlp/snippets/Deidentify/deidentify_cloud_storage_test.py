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

import deidentify_cloud_storage as deid

import google.cloud.dlp_v2
import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TXT_FILE = os.path.join(os.path.dirname(__file__), "../resources/test.txt")


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_deidentify_cloud_storage(
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value

    # Configure the mock CreateDlpJob DLP method and its behavior.
    test_job = f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job"
    mock_dlp_instance.create_dlp_job.return_value.name = test_job

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = test_job
    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    # Considering this file is present in gcs bucket.
    file = open(TXT_FILE, "r")
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

    deid.deidentify_cloud_storage(
        GCLOUD_PROJECT,
        "input_bucket",
        "output_bucket",
        ["EMAIL_ADDRESS", "PERSON_NAME", "PHONE_NUMBER"],
        "deidentify_template_name",
        "structured_deidentify_template_name",
        "image_redaction_template_name",
        "DATASET_ID",
        "TABLE_ID",
        timeout=1,
    )
    out, _ = capsys.readouterr()
    assert test_job in out
    assert "Processed Bytes" in out
    assert "Info type: EMAIL_ADDRESS" in out

    create_job_args = mock_dlp_instance.create_dlp_job.call_args
    mock_dlp_instance.create_dlp_job.assert_called_once_with(
        request=create_job_args.kwargs["request"]
    )
    mock_dlp_instance.get_dlp_job.assert_called_once_with(request={"name": test_job})
