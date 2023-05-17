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
import uuid

from googleapiclient.errors import HttpError
import pytest
from retrying import retry

import datasets


cloud_region = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

dataset_id = f"test-dataset-{uuid.uuid4()}"
destination_dataset_id = f"test-destination-dataset-{uuid.uuid4()}"
time_zone = "UTC"


def retry_if_server_exception(exception):
    return isinstance(exception, (HttpError))


@pytest.fixture(scope="module")
def test_dataset():
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=10,
        retry_on_exception=retry_if_server_exception,
    )
    def create():
        try:
            datasets.create_dataset(project_id, cloud_region, dataset_id)
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
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=10,
        retry_on_exception=retry_if_server_exception,
    )
    def clean_up():
        try:
            datasets.delete_dataset(project_id, cloud_region, dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 404 or err.resp.status == 403:
                print(f"Got exception {err.resp.status} while deleting dataset")
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def dest_dataset_id():
    yield destination_dataset_id

    # Clean up
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=10,
        retry_on_exception=retry_if_server_exception,
    )
    def clean_up():
        try:
            datasets.delete_dataset(project_id, cloud_region, destination_dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 404 or err.resp.status == 403:
                print(f"Got exception {err.resp.status} while deleting dataset")
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def crud_dataset_id():
    yield dataset_id

    # Clean up
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=10,
        retry_on_exception=retry_if_server_exception,
    )
    def clean_up():
        try:
            datasets.delete_dataset(project_id, cloud_region, dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 404 or err.resp.status == 403:
                print(f"Got exception {err.resp.status} while deleting dataset")
            else:
                raise

    clean_up()


def test_CRUD_dataset(capsys, crud_dataset_id):
    datasets.create_dataset(project_id, cloud_region, crud_dataset_id)

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=10,
        retry_on_exception=retry_if_server_exception,
    )
    def get_dataset():
        datasets.get_dataset(project_id, cloud_region, crud_dataset_id)

    get_dataset()

    datasets.list_datasets(project_id, cloud_region)

    datasets.delete_dataset(project_id, cloud_region, crud_dataset_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert "Created dataset" in out
    assert "Time zone" in out
    assert "Dataset" in out
    assert "Deleted dataset" in out


def test_patch_dataset(capsys, test_dataset):
    # To mitigate the flake with HttpErrors.
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=10,
        retry_on_exception=retry_if_server_exception,
    )
    def run_sample():
        datasets.patch_dataset(project_id, cloud_region, dataset_id, time_zone)

    run_sample()

    out, _ = capsys.readouterr()

    # Check that the patch to the time zone worked
    assert "UTC" in out


def test_deidentify_dataset(capsys, test_dataset, dest_dataset_id):
    datasets.deidentify_dataset(project_id, cloud_region, dataset_id, dest_dataset_id)

    out, _ = capsys.readouterr()

    # Check that de-identify worked
    assert "De-identified data written to" in out


def test_get_set_dataset_iam_policy(capsys, test_dataset):
    get_response = datasets.get_dataset_iam_policy(project_id, cloud_region, dataset_id)

    set_response = datasets.set_dataset_iam_policy(
        project_id,
        cloud_region,
        dataset_id,
        "serviceAccount:python-docs-samples-tests@appspot.gserviceaccount.com",
        "roles/viewer",
    )

    out, _ = capsys.readouterr()

    assert "etag" in get_response
    assert "bindings" in set_response
    assert len(set_response["bindings"]) == 1
    assert "python-docs-samples-tests" in str(set_response["bindings"])
    assert "roles/viewer" in str(set_response["bindings"])
