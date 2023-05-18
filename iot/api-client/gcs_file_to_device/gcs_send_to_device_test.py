# Copyright 2018 Google, Inc.
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

import os
import sys
import tempfile
import time
import uuid

from google.cloud import pubsub
from google.cloud import storage
import pytest
import requests

import gcs_send_to_device as gcs_to_device

# Add manager for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))  # noqa
import manager  # noqa

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

topic_id = f"test-device-events-{str(uuid.uuid4())}"
device_id = f"test-device-{str(uuid.uuid4())}"
registry_id = f"test-registry-{uuid.uuid4().hex}-{int(time.time())}"
pubsub_topic = f"projects/{project_id}/topics/{topic_id}"

cloud_region = "us-central1"
destination_file_name = "destination-file.bin"
gcs_file_name = "my-config"

storage_client = storage.Client()


@pytest.fixture(scope="module")
def test_bucket_name():
    bucket_name = f"python-docs-samples-iot-{uuid.uuid4()}"

    yield bucket_name

    bucket = storage_client.bucket(bucket_name)
    bucket.delete(force=True)


@pytest.fixture(scope="module")
def test_bucket(test_bucket_name):
    """Yields a bucket that is deleted after the test completes."""
    bucket = storage_client.bucket(test_bucket_name)

    if not bucket.exists():
        bucket = storage_client.create_bucket(test_bucket_name)

    yield bucket.name


@pytest.fixture(scope="module")
def test_blob(test_bucket):
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage_client.bucket(test_bucket)
    # Name of the blob
    blob = bucket.blob(f"iot_core_store_file_gcs-{uuid.uuid4()}")
    # Text in the blob
    blob.upload_from_string("This file on GCS will go to a device.")

    yield blob

    # Clean up
    try:
        blob.delete()
    except:  # noqa
        pass


def test_create_bucket(test_bucket_name, capsys):
    gcs_to_device.create_bucket(test_bucket_name)

    out, _ = capsys.readouterr()
    assert f"Bucket {test_bucket_name} created" in out


def test_upload_local_file(test_bucket, capsys):
    # Creates a temporary source file that gets uploaded
    # to GCS. All other tests use the blob in test_blob().
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b"This is a source file.")

        gcs_to_device.upload_local_file(test_bucket, gcs_file_name, source_file.name)

    out, _ = capsys.readouterr()
    assert f"File {source_file.name} uploaded as {gcs_file_name}." in out


def test_make_file_public(test_bucket, test_blob):
    gcs_to_device.make_file_public(test_bucket, test_blob.name)

    r = requests.get(test_blob.public_url)
    # Test for the content of the file to verify that
    # it's publicly accessible.
    assert r.text == "This file on GCS will go to a device."


def test_send_to_device(test_bucket, capsys):
    manager.create_iot_topic(project_id, topic_id)
    manager.open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic, registry_id
    )

    manager.create_unauth_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    gcs_to_device.send_to_device(
        test_bucket,
        gcs_file_name,
        destination_file_name,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        service_account_json,
    )

    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(request={"topic": topic_path})

    out, _ = capsys.readouterr()
    assert "Successfully sent file to device" in out


def test_get_state(capsys):
    manager.create_iot_topic(project_id, topic_id)
    manager.open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic, registry_id
    )

    manager.create_unauth_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    gcs_to_device.get_state(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)

    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project_id, topic_id)
    pubsub_client.delete_topic(request={"topic": topic_path})

    out, _ = capsys.readouterr()
    assert "Id" in out
    assert "Config" in out
