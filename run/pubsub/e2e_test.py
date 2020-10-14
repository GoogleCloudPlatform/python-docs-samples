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

from google.cloud import logging_v2

import pytest


SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
CLOUD_RUN_SERVICE = f"pubsub-test-{SUFFIX}"


@pytest.fixture()
def cloud_run_service():
    # Build and Deploy Cloud Run Services
    subprocess.run(
        ["gcloud", "builds", "submit", "--project", PROJECT,
         f"--substitutions=_SERVICE={CLOUD_RUN_SERVICE}",
         "--config=e2e_test_setup.yaml", "--quiet"],
        check=True
    )

    yield

    # Delete Cloud Run service and image container
    subprocess.run(
        ["gcloud", "run", "services", "delete", CLOUD_RUN_SERVICE,
         "--project", PROJECT, "--platform", "managed", "--region",
         "us-central1", "--quiet"],
        check=True
    )

    subprocess.run(
        ["gcloud", "container", "images", "delete",
         f"gcr.io/{PROJECT}/{CLOUD_RUN_SERVICE}", "--quiet"],
        check=True
    )


@pytest.fixture
def service_url(cloud_run_service):
    # Get the URL for the cloud run service
    service_url = subprocess.run(
        [
            "gcloud",
            "run",
            "--project",
            PROJECT,
            "--platform=managed",
            "--region=us-central1",
            "services",
            "describe",
            CLOUD_RUN_SERVICE,
            "--format=value(status.url)",
        ],
        stdout=subprocess.PIPE,
        check=True
    ).stdout.strip()

    yield service_url.decode()


@pytest.fixture()
def pubsub_topic(service_url):
    # Create pub/sub topic
    topic = f"e2e_{SUFFIX}"
    subprocess.run(
        ["gcloud", "pubsub", "topics", "create", topic,
         "--project", PROJECT, "--quiet"], check=True
    )

    # Create pubsub push subscription to Cloud Run Service
    # Attach service account with Cloud Run Invoker role
    # See tutorial for details on setting up service-account:
    # https://cloud.google.com/run/docs/tutorials/pubsub
    subprocess.run(
        ["gcloud", "pubsub", "subscriptions", "create", f"{topic}_sub",
         "--topic", topic, "--push-endpoint", service_url, "--project",
         PROJECT, "--push-auth-service-account",
         f"cloud-run-invoker@{PROJECT}.iam.gserviceaccount.com",
         "--quiet"], check=True
    )

    yield topic

    # Delete topic
    subprocess.run(
        ["gcloud", "pubsub", "topics", "delete", topic,
         "--project", PROJECT, "--quiet"], check=True
    )

    # Delete subscription
    subprocess.run(
        ["gcloud", "pubsub", "subscriptions", "delete", f"{topic}_sub",
         "--project", PROJECT, "--quiet"], check=True
    )


def test_end_to_end(pubsub_topic):
    # Post the message "Runner" to the topic
    subprocess.run(
        ["gcloud", "pubsub", "topics", "publish", f"{pubsub_topic}",
         "--project", PROJECT, "--message", "Runner", "--quiet"], check=True
    )

    # Check the logs for "Hello Runner"
    time.sleep(20)  # Slight delay writing to stackdriver
    client = logging_v2.LoggingServiceV2Client()
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
        iterator = client.list_log_entries(resource_names, filter_=filters)
        for entry in iterator:
            if entry.text_payload == "Hello Runner!":
                found = True
                break
        # When message found, exit loop
        if found is True:
            break
        time.sleep(5)  # Slight delay before retry

    assert found
