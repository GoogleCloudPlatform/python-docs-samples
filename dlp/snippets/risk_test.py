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
import unittest

from unittest import mock
from unittest.mock import MagicMock, Mock

import uuid

import google.cloud.bigquery
import google.cloud.dlp_v2
import google.cloud.pubsub
import pytest

import risk

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
GCLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
TABLE_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
TOPIC_ID = "dlp-test" + UNIQUE_STRING
SUBSCRIPTION_ID = "dlp-test-subscription" + UNIQUE_STRING
UNIQUE_FIELD = "Name"
REPEATED_FIELD = "Mystery"
NUMERIC_FIELD = "Age"
STRING_BOOLEAN_FIELD = "Gender"

BIGQUERY_DATASET_ID = "dlp_test_dataset" + UNIQUE_STRING
BIGQUERY_TABLE_ID = "dlp_test_table" + UNIQUE_STRING
BIGQUERY_HARMFUL_TABLE_ID = "harmful" + UNIQUE_STRING
DLP_CLIENT = google.cloud.dlp_v2.DlpServiceClient()


def mock_subscriber_client():
    class MockSubscriberClient:
        def subscription_path(self, project, subscription_id):
            return f"projects/{project}/subscriptions/{subscription_id}"

        def subscribe(self, subscription_path, callback):
            subscription = MockSubscription(callback)
            return subscription

    class MockSubscription:
        def __init__(self, callback):
            self.callback = callback

        def result(self, timeout=None):
            # Simulate the callback behavior here
            message_mock = MagicMock()
            message_mock.attributes = {"DlpJobName": "example_job"}
            self.callback(message_mock)

        def set_result(self, timeout=None):
            return None

    mock_subscriber = MockSubscriberClient()

    return mock_subscriber


def mock_clients_for_numerical_risk():
    class MockDlpClient:
        def get_dlp_job(self, request):
            # Simulate fetching DLP job results
            job_mock = Mock()
            job_mock.name = "example_job"
            # Simulate risk details and histogram
            results = job_mock.risk_details.numerical_stats_result
            results.min_value.integer_value = 1
            results.max_value.integer_value = 100
            results.quantile_values = [
                MockResult(),
                MockResult(),
            ]
            return job_mock

        def create_dlp_job(self, request):
            job_mock = Mock()
            job_mock.name = "example_job"
            return job_mock

    class MockResult:
        def __init__(self):
            self.integer_value = 27

    mock_dlp = MockDlpClient()
    dlp_mock = MagicMock(return_value=mock_dlp)
    mock_subscriber = mock_subscriber_client()

    return dlp_mock, mock_subscriber


def test_numerical_risk_analysis(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_numerical_risk()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.numerical_risk_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            NUMERIC_FIELD,
            "topic_id",
            "subscription_id",
        )

    out, _ = capsys.readouterr()
    assert "Value Range:" in out
    assert "Job name:" in out


def mock_clients_for_categorical_risk():
    class MockDlpClient:
        def get_dlp_job(self, request):
            # Simulate fetching DLP job results
            job_mock = Mock()
            job_mock.name = "example_job"
            # Simulate risk details and histogram
            job_mock.risk_details.categorical_stats_result.value_frequency_histogram_buckets = [
                MockBucket(),
                MockBucket(),
            ]
            return job_mock

        def create_dlp_job(self, request):
            job_mock = Mock()
            job_mock.name = "example_job"
            return job_mock

    class MockBucket:
        def __init__(self):
            self.value_frequency_lower_bound = 1
            self.value_frequency_upper_bound = 5
            self.bucket_size = 10
            self.bucket_values = [MockValueBucket(), MockValueBucket()]

    class MockValueBucket:
        def __init__(self):
            self.value = MockIntegerValue()
            self.count = 6

    class MockIntegerValue:
        def __init__(self):
            self.integer_value = 56

    mock_dlp = MockDlpClient()
    dlp_mock = MagicMock(return_value=mock_dlp)
    mock_subscriber = mock_subscriber_client()

    return dlp_mock, mock_subscriber


def test_categorical_risk_analysis_on_string_field(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_categorical_risk()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.categorical_risk_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            UNIQUE_FIELD,
            "topic_id",
            "subscription_id",
        )

    out, _ = capsys.readouterr()
    assert "Most common value occurs" in out
    assert "Job name:" in out


def test_categorical_risk_analysis_on_number_field(
    capsys: pytest.CaptureFixture,
) -> None:

    dlp_mock, mock_subscriber = mock_clients_for_categorical_risk()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.categorical_risk_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            NUMERIC_FIELD,
            "topic_id",
            "subscription_id",
        )

    out, _ = capsys.readouterr()
    assert "Most common value occurs" in out
    assert "Job name:" in out


def mock_clients_for_k_anonimity():
    class MockDlpClient:
        def get_dlp_job(self, request):
            # Simulate fetching DLP job results
            job_mock = Mock()
            job_mock.name = "example_job"
            # Simulate risk details and histogram
            job_mock.risk_details.k_anonymity_result.equivalence_class_histogram_buckets = [
                MockBucket(),
                MockBucket(),
            ]
            return job_mock

        def create_dlp_job(self, request):
            job_mock = Mock()
            job_mock.name = "example_job"
            return job_mock

    class MockBucket:
        def __init__(self):
            self.equivalence_class_size_lower_bound = 1
            self.equivalence_class_size_upper_bound = 5
            self.bucket_size = 10
            self.bucket_values = [MockValueBucket(), MockValueBucket()]

    class MockValueBucket:
        def __init__(self):
            self.quasi_ids_values = [MockQuasiId()]
            self.equivalence_class_size = 3

    class MockQuasiId:
        def __init__(self):
            self.value = "quasi_id_value"

    mock_dlp = MockDlpClient()
    dlp_mock = MagicMock(return_value=mock_dlp)
    mock_subscriber = mock_subscriber_client()

    return dlp_mock, mock_subscriber


def test_k_anonymity_analysis_single_field(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_k_anonimity()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.k_anonymity_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            "topic_id",
            "subscription_id",
            [NUMERIC_FIELD],
        )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Job name:" in out


def test_k_anonymity_analysis_multiple_fields(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_k_anonimity()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.k_anonymity_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            "topic_id",
            "subscription_id",
            [NUMERIC_FIELD, REPEATED_FIELD],
        )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Job name:" in out


def mock_clients_for_l_diversity():
    class MockDlpClient:
        def get_dlp_job(self, request):
            # Simulate fetching DLP job results
            job_mock = Mock()
            job_mock.name = "example_job"
            # Simulate risk details and histogram
            job_mock.risk_details.l_diversity_result.sensitive_value_frequency_histogram_buckets = [
                MockBucket(),
                MockBucket(),
            ]
            return job_mock

        def create_dlp_job(self, request):
            job_mock = Mock()
            job_mock.name = "example_job"
            return job_mock

    class MockBucket:
        def __init__(self):
            self.sensitive_value_frequency_lower_bound = 1
            self.sensitive_value_frequency_upper_bound = 5
            self.bucket_size = 10
            self.bucket_values = [MockValueBucket(), MockValueBucket()]

    class MockValueBucket:
        def __init__(self):
            self.quasi_ids_values = [MockQuasiId()]
            self.top_sensitive_values = [MockSensitiveValues()]
            self.equivalence_class_size = 1

    class MockQuasiId:
        def __init__(self):
            self.value = "quasi_id_value"

    class MockSensitiveValues:
        def __init__(self):
            self.value = "sensitive_value"
            self.count = 6

    mock_dlp = MockDlpClient()
    dlp_mock = MagicMock(return_value=mock_dlp)
    mock_subscriber = mock_subscriber_client()

    return dlp_mock, mock_subscriber


def test_l_diversity_analysis_single_field(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_l_diversity()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.l_diversity_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            "topic_id",
            "subscription_id",
            UNIQUE_FIELD,
            [NUMERIC_FIELD],
        )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Sensitive value" in out
    assert "Job name:" in out


def test_l_diversity_analysis_multiple_field(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_l_diversity()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.l_diversity_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            "topic_id",
            "subscription_id",
            UNIQUE_FIELD,
            [NUMERIC_FIELD, REPEATED_FIELD],
        )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Sensitive value" in out
    assert "Job name:" in out


def mock_clients_for_k_map():
    class MockDlpClient:
        def get_dlp_job(self, request):
            # Simulate fetching DLP job results
            job_mock = Mock()
            job_mock.name = "example_job"
            # Simulate risk details and histogram
            job_mock.risk_details.k_map_estimation_result.k_map_estimation_histogram = [
                MockBucket(),
                MockBucket(),
            ]
            return job_mock

        def create_dlp_job(self, request):
            job_mock = Mock()
            job_mock.name = "example_job"
            return job_mock

    class MockBucket:
        def __init__(self):
            self.min_anonymity = 1
            self.max_anonymity = 5
            self.bucket_size = 10
            self.bucket_values = [MockValueBucket(), MockValueBucket()]

    class MockValueBucket:
        def __init__(self):
            self.quasi_ids_values = [MockQuasiId()]
            self.estimated_anonymity = 3

    class MockQuasiId:
        def __init__(self):
            self.value = "quasi_id_value"

    mock_dlp = MockDlpClient()
    dlp_mock = MagicMock(return_value=mock_dlp)
    mock_subscriber = mock_subscriber_client()

    return dlp_mock, mock_subscriber


def test_k_map_estimate_analysis_single_field(
    capsys: pytest.CaptureFixture,
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_k_map()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.k_map_estimate_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            "topic_id",
            "subscription_id",
            [NUMERIC_FIELD],
            ["AGE"],
        )

    out, _ = capsys.readouterr()
    assert "Anonymity range:" in out
    assert "Size:" in out
    assert "Values" in out
    assert "Job name:" in out


def test_k_map_estimate_analysis_multiple_field(
    capsys: pytest.CaptureFixture
) -> None:
    dlp_mock, mock_subscriber = mock_clients_for_k_map()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        risk.k_map_estimate_analysis(
            GCLOUD_PROJECT,
            TABLE_PROJECT,
            BIGQUERY_DATASET_ID,
            BIGQUERY_HARMFUL_TABLE_ID,
            "topic_id",
            "subscription_id",
            [NUMERIC_FIELD, STRING_BOOLEAN_FIELD],
            ["AGE", "GENDER"],
        )

    out, _ = capsys.readouterr()
    assert "Anonymity range:" in out
    assert "Size:" in out
    assert "Values" in out
    assert "Job name:" in out


def test_k_map_estimate_analysis_quasi_ids_info_types_equal() -> None:
    dlp_mock, mock_subscriber = mock_clients_for_k_map()
    with unittest.mock.patch(
        "google.cloud.pubsub.SubscriberClient", return_value=mock_subscriber
    ), unittest.mock.patch(
        "google.cloud.dlp_v2.DlpServiceClient", dlp_mock
    ):
        with pytest.raises(ValueError):
            risk.k_map_estimate_analysis(
                GCLOUD_PROJECT,
                TABLE_PROJECT,
                BIGQUERY_DATASET_ID,
                BIGQUERY_HARMFUL_TABLE_ID,
                "topic_id",
                "subscription_id",
                [NUMERIC_FIELD, STRING_BOOLEAN_FIELD],
                ["AGE"],
            )


@mock.patch("google.cloud.dlp_v2.DlpServiceClient")
def test_k_anonymity_with_entity_id(
    dlp_client: MagicMock,
    capsys: pytest.CaptureFixture,
) -> None:

    # Configure the mock DLP client and its behavior.
    mock_dlp_instance = dlp_client.return_value
    # Configure the mock CreateDlpJob DLP method and its behavior.
    mock_dlp_instance.create_dlp_job.return_value.name = f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job'

    # Configure the mock GetDlpJob DLP method and its behavior.
    mock_job = mock_dlp_instance.get_dlp_job.return_value
    mock_job.name = f'projects/{GCLOUD_PROJECT}/dlpJobs/test_job'
    mock_job.state = google.cloud.dlp_v2.DlpJob.JobState.DONE

    # Mocking value for quasi_id ("Age", for instance)
    mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values.quasi_ids_values = [
        MagicMock(string_value="[\"27\"]")
    ]
    quasi_ids_values = \
        mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values.quasi_ids_values

    mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values = [
        MagicMock(quasi_ids_values=quasi_ids_values, equivalence_class_size=1)
    ]
    bucket_values = mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets.bucket_values

    mock_job.risk_details.k_anonymity_result.equivalence_class_histogram_buckets = [
        MagicMock(equivalence_class_size_lower_bound=1, equivalence_class_size_upper_bound=1, bucket_size=1,
                  bucket_values=bucket_values, bucket_value_count=1)
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
