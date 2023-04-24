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

import backoff
from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
import pytest


SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
CLOUD_RUN_SERVICE = f"pubsub-test-{SUFFIX}"
TOPIC = f"pubsub-test_{SUFFIX}"
IMAGE_NAME = f"gcr.io/{PROJECT}/pubsub-test-{SUFFIX}"

@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def build_container_image(image_name, project):
    """Build container image for Cloud Run deployment."""
    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            "--tag",
            image_name,
            "--project",
            project,
            "--quiet",
        ]
    )


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def delete_container_image(image_name, project):
    """Delete container image."""
    subprocess.check_call(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            image_name,
            "--quiet",
            "--project",
            project,
        ]
    )


@pytest.fixture(scope='module')
def container_image():
    try:
        build_container_image(IMAGE_NAME, PROJECT)
        yield IMAGE_NAME
    finally:
        delete_container_image(IMAGE_NAME, PROJECT)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def deploy_image(cloud_run_service, container_image, project):
    """Deploy image to Cloud Run."""
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "deploy",
            cloud_run_service,
            "--image",
            container_image,
            "--region=us-central1",
            "--project",
            project,
            "--platform=managed",
            "--no-allow-unauthenticated",
        ]
    )


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def delete_service(cloud_run_service, project):
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            cloud_run_service,
            "--platform=managed",
            "--region=us-central1",
            "--quiet",
            "--async",
            "--project",
            project,
        ]
    )


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def get_service_url(cloud_run_service, project):
    return subprocess.run(
        [
            "gcloud",
            "run",
            "--project",
            project,
            "services",
            "describe",
            cloud_run_service,
            "--platform=managed",
            "--region=us-central1",
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.strip().decode()


@pytest.fixture(scope='module')
def service_url(container_image):
    try:
        deploy_image(CLOUD_RUN_SERVICE, container_image, PROJECT)
        yield get_service_url(CLOUD_RUN_SERVICE, PROJECT)
    finally:
        delete_service(CLOUD_RUN_SERVICE, PROJECT)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def create_topic(project, topic):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    publisher.create_topic(request={"name": topic_path})
    return TOPIC


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def delete_topic(project, topic):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    try:
        publisher.delete_topic(request={"topic": topic_path})
    except NotFound:
        print("Topic not found, it was either never created or was already deleted.")


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def create_subscription(pubsub_topic, service_url):
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


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def delete_subscription(pubsub_topic):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_id = f"{pubsub_topic}_sub"
    subscription_path = subscriber.subscription_path(PROJECT, subscription_id)
    # delete subscription
    with subscriber:
        try:
            subscriber.delete_subscription(request={"subscription": subscription_path})
        except NotFound:
            print(
                "Unable to delete - subscription either never created or already deleted."
            )


@pytest.fixture(scope='module')
def pubsub_topic(service_url):
    try:
        topic = create_topic(PROJECT, TOPIC)
        create_subscription(topic, service_url)
        yield topic 
    finally:
        delete_topic(PROJECT, TOPIC)
        delete_subscription(topic)


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
