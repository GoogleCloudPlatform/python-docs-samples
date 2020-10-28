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

# This tests the Pub/Sub image processing sample

import os
import subprocess
import time
import uuid

from google.cloud import storage
from google.cloud.storage import Blob, notification

import pytest


SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
CLOUD_RUN_SERVICE = f"image-proc-{SUFFIX}"
INPUT_BUCKET = f"image-proc-input-{SUFFIX}"
OUTPUT_BUCKET = f"image-proc-output-{SUFFIX}"


@pytest.fixture()
def cloud_run_service():
    # Build and Deploy Cloud Run Services
    subprocess.run(
        ["gcloud", "builds", "submit", "--project", PROJECT,
         f"--substitutions=_SERVICE={CLOUD_RUN_SERVICE},_OUTPUT_BUCKET={OUTPUT_BUCKET}",
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
    topic = f"image_proc_{SUFFIX}"
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
         f"cloud-run-invoker@{PROJECT}.iam.gserviceaccount.com", "--quiet"], check=True
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


@pytest.fixture()
def storage_buckets(pubsub_topic):
    # Create GCS Buckets
    storage_client = storage.Client()
    storage_client.create_bucket(INPUT_BUCKET)
    storage_client.create_bucket(OUTPUT_BUCKET)

    # Get input and output buckets
    input_bucket = storage_client.get_bucket(INPUT_BUCKET)
    output_bucket = storage_client.get_bucket(OUTPUT_BUCKET)

    # Create pub/sub notification on input_bucket
    notification.BucketNotification(input_bucket, topic_name=pubsub_topic,
                                    topic_project=PROJECT, payload_format="JSON_API_V1").create()

    yield input_bucket, output_bucket

    # Delete GCS buckets
    input_bucket.delete(force=True)
    output_bucket.delete(force=True)


def test_end_to_end(storage_buckets):
    # Upload image to the input bucket
    input_bucket = storage_buckets[0]
    output_bucket = storage_buckets[1]

    blob = Blob("zombie.jpg", input_bucket)
    blob.upload_from_filename("test-images/zombie.jpg", content_type="image/jpeg")

    # Wait for image processing to complete
    time.sleep(30)

    for x in range(10):
        # Check for blurred image in output bucket
        output_blobs = list(output_bucket.list_blobs())
        if len(output_blobs) > 0:
            break

        time.sleep(5)

    assert len(output_blobs) > 0
