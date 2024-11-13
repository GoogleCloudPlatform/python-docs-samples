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
BIGQUERY_TABLE_ID = "dlp_test_table" + UNIQUE_STRING
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


@pytest.fixture(scope="module")
def bigquery_project() -> Iterator[str]:
    # Adds test Bigquery data, yields the project ID and then tears down.

    bigquery_client = google.cloud.bigquery.Client()

    dataset_ref = bigquery_client.dataset(BIGQUERY_DATASET_ID)
    dataset = google.cloud.bigquery.Dataset(dataset_ref)
    try:
        dataset = bigquery_client.create_dataset(dataset)
    except google.api_core.exceptions.Conflict:
        dataset = bigquery_client.get_dataset(dataset)
    table_ref = dataset_ref.table(BIGQUERY_TABLE_ID)
    table = google.cloud.bigquery.Table(table_ref)

    harmful_table_ref = dataset_ref.table(BIGQUERY_HARMFUL_TABLE_ID)
    harmful_table = google.cloud.bigquery.Table(harmful_table_ref)

    table.schema = (
        google.cloud.bigquery.SchemaField("Name", "STRING"),
        google.cloud.bigquery.SchemaField("Comment", "STRING"),
    )

    harmful_table.schema = (
        google.cloud.bigquery.SchemaField("Name", "STRING", "REQUIRED"),
        google.cloud.bigquery.SchemaField("TelephoneNumber", "STRING", "REQUIRED"),
        google.cloud.bigquery.SchemaField("Mystery", "STRING", "REQUIRED"),
        google.cloud.bigquery.SchemaField("Age", "INTEGER", "REQUIRED"),
        google.cloud.bigquery.SchemaField("Gender", "STRING"),
        google.cloud.bigquery.SchemaField("RegionCode", "STRING"),
    )

    try:
        table = bigquery_client.create_table(table)
    except google.api_core.exceptions.Conflict:
        table = bigquery_client.get_table(table)

    try:
        harmful_table = bigquery_client.create_table(harmful_table)
    except google.api_core.exceptions.Conflict:
        harmful_table = bigquery_client.get_table(harmful_table)

    rows_to_insert = [("Gary Smith", "My email is gary@example.com")]
    harmful_rows_to_insert = [
        (
            "Gandalf",
            "(123) 456-7890",
            "4231 5555 6781 9876",
            27,
            "Male",
            "US",
        ),
        (
            "Dumbledore",
            "(313) 337-1337",
            "6291 8765 1095 7629",
            27,
            "Male",
            "US",
        ),
        ("Joe", "(452) 123-1234", "3782 2288 1166 3030", 35, "Male", "US"),
        ("James", "(567) 890-1234", "8291 3627 8250 1234", 19, "Male", "US"),
        (
            "Marie",
            "(452) 123-1234",
            "8291 3627 8250 1234",
            35,
            "Female",
            "US",
        ),
        (
            "Carrie",
            "(567) 890-1234",
            "2253 5218 4251 4526",
            35,
            "Female",
            "US",
        ),
    ]

    bigquery_client.insert_rows(table, rows_to_insert)
    bigquery_client.insert_rows(harmful_table, harmful_rows_to_insert)
    yield GCLOUD_PROJECT

    bigquery_client.delete_dataset(dataset_ref, delete_contents=True)


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_k_anonymity_analysis_single_field(
    topic_id: str,
    subscription_id: str,
    bigquery_project: str,
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
    bigquery_project: str,
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
