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
from typing import Iterator

import uuid

import google.cloud.bigquery
import google.cloud.dlp_v2
import google.cloud.pubsub

import k_anonymity as risk

import pytest


UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
GCLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
TABLE_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
TOPIC_ID = "dlp-test" + UNIQUE_STRING
SUBSCRIPTION_ID = "dlp-test-subscription" + UNIQUE_STRING
REPEATED_FIELD = "Mystery"
NUMERIC_FIELD = "Age"

BIGQUERY_DATASET_ID = "dlp_test_dataset" + UNIQUE_STRING
BIGQUERY_HARMFUL_TABLE_ID = "harmful" + UNIQUE_STRING
DLP_CLIENT = google.cloud.dlp_v2.DlpServiceClient()


# Create new custom topic/subscription
# We observe sometimes all the tests in this file fail. In a
# hypothesis where DLP service somehow loses the connection to the
# topic, now we use function scope for Pub/Sub fixtures.
@pytest.fixture(scope="module")
def topic_id() -> Iterator[str]:
    # Creates a pubsub topic, and tears it down.
    publisher = google.cloud.pubsub.PublisherClient()
    topic_path = publisher.topic_path(GCLOUD_PROJECT, TOPIC_ID)
    try:
        publisher.create_topic(request={"name": topic_path})
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield TOPIC_ID

    publisher.delete_topic(request={"topic": topic_path})


@pytest.fixture(scope="module")
def subscription_id(topic_id: str) -> Iterator[str]:
    # Subscribes to a topic.
    subscriber = google.cloud.pubsub.SubscriberClient()
    topic_path = subscriber.topic_path(GCLOUD_PROJECT, topic_id)
    subscription_path = subscriber.subscription_path(GCLOUD_PROJECT, SUBSCRIPTION_ID)
    try:
        subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
    except google.api_core.exceptions.AlreadyExists:
        pass

    yield SUBSCRIPTION_ID

    subscriber.delete_subscription(request={"subscription": subscription_path})


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_k_anonymity_analysis_single_field(
    topic_id: str,
    subscription_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    risk.k_anonymity_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        BIGQUERY_DATASET_ID,
        BIGQUERY_HARMFUL_TABLE_ID,
        topic_id,
        subscription_id,
        [NUMERIC_FIELD],
    )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Job name:" in out
    for line in str(out).split("\n"):
        if "Job name" in line:
            job_name = line.split(":")[1].strip()
            DLP_CLIENT.delete_dlp_job(name=job_name)


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_k_anonymity_analysis_multiple_fields(
    topic_id: str,
    subscription_id: str,
    capsys: pytest.CaptureFixture,
) -> None:
    risk.k_anonymity_analysis(
        GCLOUD_PROJECT,
        TABLE_PROJECT,
        BIGQUERY_DATASET_ID,
        BIGQUERY_HARMFUL_TABLE_ID,
        topic_id,
        subscription_id,
        [NUMERIC_FIELD, REPEATED_FIELD],
    )

    out, _ = capsys.readouterr()
    assert "Quasi-ID values:" in out
    assert "Class size:" in out
    assert "Job name:" in out
    for line in str(out).split("\n"):
        if "Job name" in line:
            job_name = line.split(":")[1].strip()
            DLP_CLIENT.delete_dlp_job(name=job_name)
