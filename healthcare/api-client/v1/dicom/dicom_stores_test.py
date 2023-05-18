# Copyright 2018 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import uuid

import backoff
from google.cloud import pubsub_v1
from googleapiclient.errors import HttpError
import pytest

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "datasets"))  # noqa
import datasets  # noqa
import dicom_stores  # noqa


location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

dataset_id = f"test_dataset-{uuid.uuid4()}"
dicom_store_id = f"test_dicom_store_{uuid.uuid4()}"
pubsub_topic = f"test_pubsub_topic_{uuid.uuid4()}"

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
bucket = os.environ["CLOUD_STORAGE_BUCKET"]
dcm_file_name = "dicom_00000001_000.dcm"
content_uri = bucket + "/" + dcm_file_name
dcm_file = os.path.join(RESOURCES, dcm_file_name)


@pytest.fixture(scope="module")
def test_dataset():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            datasets.create_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(f"Got exception {err.resp.status} while creating dataset")
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            datasets.delete_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 403:
                print(f"Got exception {err.resp.status} while deleting dataset")
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def test_dicom_store():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            dicom_stores.create_dicom_store(
                project_id, location, dataset_id, dicom_store_id
            )
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(
                    "Got exception {} while creating DICOM store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            dicom_stores.delete_dicom_store(
                project_id, location, dataset_id, dicom_store_id
            )
        except HttpError as err:
            # The API returns 404 when the DICOM store doesn't exist.
            # The API returns 403 when the dataset doesn't exist, so
            # if we try to delete a DICOM store when the parent dataset
            # doesn't exist, the server will return a 403.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting DICOM store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def crud_dicom_store_id():
    yield dicom_store_id

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            dicom_stores.delete_dicom_store(
                project_id, location, dataset_id, dicom_store_id
            )
        except HttpError as err:
            # The API returns 404 when the DICOM store doesn't exist.
            # The API returns 403 when the dataset doesn't exist, so
            # if we try to delete a DICOM store when the parent dataset
            # doesn't exist, the server will return a 403.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting DICOM store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def test_pubsub_topic():
    pubsub_client = pubsub_v1.PublisherClient()
    # Create the Pub/Sub topic
    topic_path = pubsub_client.topic_path(project_id, pubsub_topic)
    pubsub_client.create_topic(request={"name": topic_path})

    yield pubsub_topic

    # Delete the Pub/Sub topic
    pubsub_client.delete_topic(request={"topic": topic_path})


def test_CRUD_dicom_store(test_dataset, crud_dicom_store_id, capsys):
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        dicom_stores.create_dicom_store(
            project_id, location, dataset_id, crud_dicom_store_id
        )

    create()

    dicom_stores.get_dicom_store(project_id, location, dataset_id, crud_dicom_store_id)

    dicom_stores.list_dicom_stores(project_id, location, dataset_id)

    dicom_stores.delete_dicom_store(
        project_id, location, dataset_id, crud_dicom_store_id
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert "Created DICOM store" in out
    assert "name" in out
    assert "dicomStores" in out
    assert "Deleted DICOM store" in out


def test_patch_dicom_store(test_dataset, test_dicom_store, test_pubsub_topic, capsys):
    dicom_stores.patch_dicom_store(
        project_id, location, dataset_id, dicom_store_id, test_pubsub_topic
    )

    out, _ = capsys.readouterr()

    assert "Patched DICOM store" in out


def test_import_dicom_instance(test_dataset, test_dicom_store, capsys):
    dicom_stores.import_dicom_instance(
        project_id, location, dataset_id, dicom_store_id, content_uri
    )

    out, _ = capsys.readouterr()

    assert "Imported DICOM instance" in out


def test_export_dicom_instance(test_dataset, test_dicom_store, capsys):
    dicom_stores.export_dicom_instance(
        project_id, location, dataset_id, dicom_store_id, bucket
    )

    out, _ = capsys.readouterr()

    assert "Exported DICOM instance" in out


def test_get_set_dicom_store_iam_policy(test_dataset, test_dicom_store, capsys):
    get_response = dicom_stores.get_dicom_store_iam_policy(
        project_id, location, dataset_id, dicom_store_id
    )

    set_response = dicom_stores.set_dicom_store_iam_policy(
        project_id,
        location,
        dataset_id,
        dicom_store_id,
        "serviceAccount:python-docs-samples-tests@appspot.gserviceaccount.com",
        "roles/viewer",
    )

    out, _ = capsys.readouterr()

    assert "etag" in get_response
    assert "bindings" in set_response
    assert len(set_response["bindings"]) == 1
    assert "python-docs-samples-tests" in str(set_response["bindings"])
    assert "roles/viewer" in str(set_response["bindings"])
