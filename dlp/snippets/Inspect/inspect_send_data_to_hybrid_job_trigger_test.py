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

import inspect_send_data_to_hybrid_job_trigger as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_inspect_data_to_hybrid_job_trigger(
    dlp_client: MagicMock, capsys: pytest.CaptureFixture
) -> None:
    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value

    # Configure the mock ActivateJobTrigger DLP method and its behavior.
    mock_dlp_instance.activate_job_trigger.return_value.name = "test_job"

    # Configure the mock HybridInspectJobTrigger DLP method and its behavior.
    mock_dlp_instance.hybrid_inspect_job_trigger.return_value = ""

    # The string to inspect.
    content_string = "My email is test@example.org"

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = "test_job"
    mock_job.inspect_details.result.processed_bytes = len(content_string)
    mock_job.inspect_details.result.info_type_stats.info_type.name = "EMAIL_ADDRESS"
    finding = mock_job.inspect_details.result.info_type_stats.info_type

    mock_job.inspect_details.result.info_type_stats = [
        MagicMock(info_type=finding, count=1),
    ]

    # Call the method.
    inspect_content.inspect_data_to_hybrid_job_trigger(
        GCLOUD_PROJECT,
        "test_trigger_id",
        content_string,
    )

    out, _ = capsys.readouterr()
    assert "Job name:" in out
    assert "Info type: EMAIL_ADDRESS" in out

    mock_dlp_instance.hybrid_inspect_job_trigger.assert_called_once()
    mock_dlp_instance.activate_job_trigger.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()
