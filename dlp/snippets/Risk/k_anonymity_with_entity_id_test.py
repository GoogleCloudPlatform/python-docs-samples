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

import k_anonymity_with_entity_id as risk

import pytest

GCLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_k_anonymity_with_entity_id(
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
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

    # Mocking value for quasi_id ("Age", for instance)
    mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values.quasi_ids_values = [
        MagicMock(string_value='["27"]')
    ]
    quasi_ids_values = (
        mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values.quasi_ids_values
    )

    mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values = [
        MagicMock(quasi_ids_values=quasi_ids_values, equivalence_class_size=1)
    ]
    bucket_values = (
        mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values
    )

    mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets = [
        MagicMock(
            equivalence_class_size_lower_bound=1,
            equivalence_class_size_upper_bound=1,
            bucket_size=1,
            bucket_values=bucket_values,
            bucket_value_count=1,
        )
    ]

    # Call the sample function considering "Name" as entity_id and "Age" as quasi_id.
    risk.k_anonymity_with_entity_id(
        GCLOUD_PROJECT,
        "SOURCE_TABLE_PROJECT",
        "SOURCE_DATASET_ID",
        "SOURCE_TABLE_ID",
        "Name",
        ["Age"],
        "OUTPUT_TABLE_PROJECT",
        "OUTPUT_DATASET_ID",
        "OUTPUT_TABLE_ID",
    )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Job name:" in out

    mock_dlp_instance.create_dlp_job.assert_called_once()
    mock_dlp_instance.get_dlp_job.assert_called_once()
