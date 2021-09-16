# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import pathlib
import re
from typing import Generator
import uuid

from google.api_core.exceptions import NotFound
from google.cloud import dataproc_v1, storage
from google.cloud.pubsublite import AdminClient, Subscription, Topic
from google.cloud.pubsublite.types import (
    BacklogLocation,
    CloudRegion,
    CloudZone,
    SubscriptionPath,
    TopicPath,
)
import pytest

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
PROJECT_NUMBER = os.environ["GOOGLE_CLOUD_PROJECT_NUMBER"]
CLOUD_REGION = "us-west1"
ZONE_ID = "a"
CLUSTER_ID = os.environ["PUBSUBLITE_CLUSTER_ID"]
BUCKET = os.environ["PUBSUBLITE_BUCKET_ID"]
UUID = uuid.uuid4().hex
TOPIC_ID = "spark-streaming-topic-" + UUID
SUBSCRIPTION_ID = "spark-streaming-subscription-" + UUID
PERMANENT_TOPIC_ID = "spark-streaming-topic"
CURRENT_DIR = pathlib.Path(__file__).parent.resolve()


@pytest.fixture(scope="module")
def client() -> Generator[AdminClient, None, None]:
    yield AdminClient(CLOUD_REGION)


@pytest.fixture(scope="module")
def topic(client: AdminClient) -> Generator[Topic, None, None]:
    location = CloudZone(CloudRegion(CLOUD_REGION), ZONE_ID)
    topic_path = TopicPath(PROJECT_NUMBER, location, TOPIC_ID)

    # A topic of 2 partitions, each of size 30 GiB, publish throughput
    # capacity per partition to 4 MiB/s, and subscribe throughput
    # capacity per partition to 8 MiB/s.
    topic = Topic(
        name=str(topic_path),
        partition_config=Topic.PartitionConfig(
            count=2,
            capacity=Topic.PartitionConfig.Capacity(
                publish_mib_per_sec=4, subscribe_mib_per_sec=8,
            ),
        ),
        retention_config=Topic.RetentionConfig(
            per_partition_bytes=30 * 1024 * 1024 * 1024,
        ),
    )

    try:
        response = client.get_topic(topic.name)
    except NotFound:
        response = client.create_topic(topic)

    yield response

    try:
        client.delete_topic(response.name)
    except NotFound as e:
        print(e.message)


@pytest.fixture(scope="module")
def subscription(client: AdminClient) -> Generator[Subscription, None, None]:
    location = CloudZone(CloudRegion(CLOUD_REGION), ZONE_ID)
    subscription_path = SubscriptionPath(PROJECT_NUMBER, location, SUBSCRIPTION_ID)

    subscription = Subscription(
        name=str(subscription_path),
        topic=f"projects/{PROJECT_NUMBER}/locations/{location}/topics/{PERMANENT_TOPIC_ID}",
        delivery_config=Subscription.DeliveryConfig(
            delivery_requirement=Subscription.DeliveryConfig.DeliveryRequirement.DELIVER_IMMEDIATELY,
        ),
    )

    try:
        response = client.get_subscription(subscription.name)
    except NotFound:
        # This subscription will start receiving the first message in the topic.
        response = client.create_subscription(subscription, BacklogLocation.BEGINNING)
    yield response
    try:
        client.delete_subscription(response.name)
    except NotFound as e:
        print(e.message)


def pyfile(source_file: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)
    destination_blob_name = os.path.join(UUID, source_file)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file)
    return "gs://" + blob.bucket.name + "/" + blob.name


def test_spark_streaming_to_pubsublite(topic: Topic) -> None:
    from google.cloud.dataproc_v1.types import LoggingConfig

    # Create a Dataproc job client.
    job_client = dataproc_v1.JobControllerClient(
        client_options={
            "api_endpoint": "{}-dataproc.googleapis.com:443".format(CLOUD_REGION)
        }
    )

    # Create the job config.
    job = {
        "placement": {"cluster_name": CLUSTER_ID},
        "pyspark_job": {
            "main_python_file_uri": pyfile("spark_streaming_to_pubsublite_example.py"),
            "jar_file_uris": [
                "gs://spark-lib/pubsublite/pubsublite-spark-sql-streaming-LATEST-with-dependencies.jar"
            ],
            "properties": {"spark.master": "yarn"},
            "logging_config": {"driver_log_levels": {"root": LoggingConfig.Level.INFO}},
            "args": [
                f"--project_number={PROJECT_NUMBER}",
                f"--location={CLOUD_REGION}-{ZONE_ID}",
                f"--topic_id={TOPIC_ID}",
            ],
        },
    }

    operation = job_client.submit_job_as_operation(
        request={
            "project_id": PROJECT_ID,
            "region": CLOUD_REGION,
            "job": job,
            "request_id": "write-" + UUID,
        }
    )
    response = operation.result()

    # Dataproc job output gets saved to the Google Cloud Storage bucket
    # allocated to the job. Use a regex to obtain the bucket and blob info.
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
        storage.Client()
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_text()
    )

    assert "Committed 1 messages for epochId" in output


def test_spark_streaming_from_pubsublite(subscription: Subscription) -> None:
    from google.cloud.dataproc_v1.types import LoggingConfig

    # Create a Dataproc job client.
    job_client = dataproc_v1.JobControllerClient(
        client_options={
            "api_endpoint": "{}-dataproc.googleapis.com:443".format(CLOUD_REGION)
        }
    )

    # Create the job config.
    job = {
        "placement": {"cluster_name": CLUSTER_ID},
        "pyspark_job": {
            "main_python_file_uri": pyfile(
                "spark_streaming_from_pubsublite_example.py"
            ),
            "jar_file_uris": [
                "gs://spark-lib/pubsublite/pubsublite-spark-sql-streaming-LATEST-with-dependencies.jar"
            ],
            "properties": {"spark.master": "yarn"},
            "logging_config": {"driver_log_levels": {"root": LoggingConfig.Level.INFO}},
            "args": [
                f"--project_number={PROJECT_NUMBER}",
                f"--location={CLOUD_REGION}-{ZONE_ID}",
                f"--subscription_id={SUBSCRIPTION_ID}",
            ],
        },
    }

    operation = job_client.submit_job_as_operation(
        request={
            "project_id": PROJECT_ID,
            "region": CLOUD_REGION,
            "job": job,
            "request_id": "read-" + UUID,
        }
    )
    response = operation.result()

    # Dataproc job output gets saved to the Google Cloud Storage bucket
    # allocated to the job. Use a regex to obtain the bucket and blob info.
    matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    output = (
        storage.Client()
        .get_bucket(matches.group(1))
        .blob(f"{matches.group(2)}.000000000")
        .download_as_text()
    )

    assert "Batch: 0\n" in output
    assert (
        "+--------------------+---------+------+----+------+"
        + "--------------------+--------------------+----------+\n"
        + "|        subscription|partition|offset| key|  data"
        + "|   publish_timestamp|     event_timestamp|attributes|\n"
        + "+--------------------+---------+------+----+------+"
        + "--------------------+--------------------+----------+\n"
        + "|projects/10126164...|        0|     0|[34]|353534"
        + "|2021-09-15 21:55:...|2021-09-15 00:04:...|        []|\n"
        in output
    )
