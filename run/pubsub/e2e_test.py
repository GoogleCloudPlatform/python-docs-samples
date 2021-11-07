# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This tests the Pub/Sub to Cloud Run integration

import datetime
import os
import subprocess
import time
import uuid

from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client


import pytest


SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
CLOUD_RUN_SERVICE = f"pubsub-test-{SUFFIX}"
TOPIC = f"pubsub-test_{SUFFIX}"
IMAGE_NAME = f"gcr.io/{PROJECT}/pubsub-test-{SUFFIX}"


@pytest.fixture
def container_image():
    # Build container image for Cloud Run deployment
    subprocess.run(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            IMAGE_NAME,
            "--project",
            PROJECT,
            "--quiet",
        ],
        check=True,
    )
    yield IMAGE_NAME

    # Delete container image
    subprocess.run(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            IMAGE_NAME,
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def deployed_service(container_image):
    # Deploy image to Cloud Run

    subprocess.run(
        [
            "gcloud",
            "run",
            "deploy",
            CLOUD_RUN_SERVICE,
            "--image",
            container_image,
            "--region=us-central1",
            "--project",
            PROJECT,
            "--platform=managed",
            "--no-allow-unauthenticated",
        ],
        check=True,
    )

    yield CLOUD_RUN_SERVICE

    subprocess.run(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            CLOUD_RUN_SERVICE,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--project",
            PROJECT,
        ],
        check=True,
    )


@pytest.fixture
def service_url(deployed_service):
    # Get the URL for the cloud run service
    service_url = subprocess.run(
        [
            "gcloud",
            "run",
            "--project",
            PROJECT,
            "services",
            "describe",
            CLOUD_RUN_SERVICE,
            "--platform=managed",
            "--region=us-central1",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.strip()

    yield service_url.decode()


@pytest.fixture()
def pubsub_topic():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, TOPIC)
    publisher.create_topic(request={"name": topic_path})
    yield TOPIC
    try:
        publisher.delete_topic(request={"topic": topic_path})
    except NotFound:
        print("Topic not found, it was either never created or was already deleted.")


@pytest.fixture(autouse=True)
def pubsub_subscription(pubsub_topic, service_url):
    # Create pubsub push subscription to Cloud Run Service
    # Attach service account with Cloud Run Invoker role
    # See tutorial for details on setting up service-account:
    # https://cloud.google.com/run/docs/tutorials/pubsub
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    subscription_id = f"{pubsub_topic}_sub"
    topic_path = publisher.topic_path(PROJECT, pubsub_topic)
    subscription_path = subscriber.subscription_path(PROJECT, subscription_id)
    push_config = pubsub_v1.types.PushConfig(
        push_endpoint=service_url,
        oidc_token=pubsub_v1.types.PushConfig.OidcToken(
            service_account_email=f"cloud-run-invoker@{PROJECT}.iam.gserviceaccount.com"
        ),
    )

    # wrapping in 'with' block automatically calls close on gRPC channel
    with subscriber:
        subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "push_config": push_config,
            }
        )
    yield
    subscriber = pubsub_v1.SubscriberClient()

    # delete subscription
    with subscriber:
        try:
            subscriber.delete_subscription(request={"subscription": subscription_path})
        except NotFound:
            print(
                "Unable to delete - subscription either never created or already deleted."
            )


def test_end_to_end(pubsub_topic):
    # Post the message "Runner" to the topic
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, pubsub_topic)
    message = "Runner"
    data = message.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    future.result()

    # Check the logs for "Hello Runner"
    time.sleep(20)  # Slight delay writing to stackdriver
    client = LoggingServiceV2Client()
    resource_names = [f"projects/{PROJECT}"]

    # We add timestamp for making the query faster.
    now = datetime.datetime.now(datetime.timezone.utc)
    filter_date = now - datetime.timedelta(minutes=1)
    filters = (
        f"timestamp>=\"{filter_date.isoformat('T')}\" "
        "resource.type=cloud_run_revision "
        f"AND resource.labels.service_name={CLOUD_RUN_SERVICE} "
    )

    # Retry a maximum number of 10 times to find results in stackdriver
    found = False
    for x in range(10):
        iterator = client.list_log_entries({"resource_names": resource_names, "filter": filters})
        for entry in iterator:
            if entry.text_payload == "Hello Runner!":
                found = True
                break
        # When message found, exit loop
        if found is True:
            break
        time.sleep(5)  # Slight delay before retry

    assert found
