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
import random

from unittest import mock
from unittest.mock import MagicMock

import google.cloud.dlp_v2
import google.cloud.pubsub

import inspect_bigquery_with_sampling as inspect_content

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def mock_job_and_subscriber(
    mock_dlp_instance: MagicMock,
    mock_subscriber_instance: MagicMock,
    dlp_job_path: str,
    finding_name: str = None,
    finding_count: int = None,
):
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = dlp_job_path

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = dlp_job_path
    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    # mock result of GetDlpJob DLP method.
    if finding_name:
        finding = mock_job.inspect_details.result.info_type_stats.info_type
        finding.name = finding_name
        mock_job.inspect_details.result.info_type_stats = [
            MagicMock(info_type=finding, count=finding_count),
        ]
    else:
        mock_job.inspect_details.result.info_type_stats = None

    # Mock class for google.cloud.pubsub.subscriber.message.Message
    class MockMessage:
        def __init__(self, data, attributes=None):
            self.data = data
            self.attributes = attributes or {}

        def ack(self):
            pass

    # Replace the real subscribe logic with a custom side effect
    def mock_subscribe(*args, **kwargs):
        # Get the callback function from the arguments.
        callback = kwargs.get("callback")

        # In this example, we'll call the callback function with a mock message
        message = MockMessage(args, {"DlpJobName": dlp_job_path})
        callback(message)

    # Patch the original method with the mock function
    mock_subscriber_instance.subscribe = mock_subscribe


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
@mock.patch("google.cloud.pubsub.SubscriberClient")
def test_inspect_bigquery_with_sampling(
    subscriber_client: MagicMock,
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:
    # Mock DLP client and subscriber client along with their behavior
    mock_dlp_instance = dlp_client.return_value
    mock_subscriber_instance = subscriber_client.return_value
    mock_job_and_subscriber(
        mock_dlp_instance,
        mock_subscriber_instance,
        f"projects/{GCLOUD_PROJECT}/dlpJobs/test_job",
        "PERSON_NAME",
        random.randint(0, 1000),
    )

    # Call the sample.
    inspect_content.inspect_bigquery_table_with_sampling(
        GCLOUD_PROJECT,
        "topic_id",
        "subscription_id",
        timeout=1,
    )

    out, _ = capsys.readouterr()
    assert "Inspection operation started" in out
    assert "Job name:" in out
    assert "Info type: PERSON_NAME" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()
