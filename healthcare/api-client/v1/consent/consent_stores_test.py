# Copyright 2022 Google LLC
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
from googleapiclient.errors import HttpError
import pytest

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "datasets"))  # noqa
import datasets  # noqa
import consent_stores  # noqa


location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

dataset_id = f"test_dataset-{uuid.uuid4()}"
consent_store_id = f"test_consent_store_{uuid.uuid4()}"

default_consent_ttl = "86400s"


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
def test_consent_store():
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        try:
            consent_stores.create_consent_store(
                project_id, location, dataset_id, consent_store_id
            )
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(
                    "Got exception {} while creating consent store".format(
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
            consent_stores.delete_consent_store(
                project_id, location, dataset_id, consent_store_id
            )
        except HttpError as err:
            # The API returns 404 when the consent store doesn't exist.
            # The API returns 403 when the dataset doesn't exist, so
            # if we try to delete a consent store when the parent dataset
            # doesn't exist, the server will return a 403.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting consent store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def crud_consent_store_id():
    yield consent_store_id

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def clean_up():
        try:
            consent_stores.delete_consent_store(
                project_id, location, dataset_id, consent_store_id
            )
        except HttpError as err:
            # The API returns 404 when the consent store doesn't exist.
            # The API returns 403 when the dataset doesn't exist, so
            # if we try to delete a consent store when the parent dataset
            # doesn't exist, the server will return a 403.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting consent store".format(
                        err.resp.status
                    )
                )
            else:
                raise

    clean_up()


def test_CRUD_consent_store(test_dataset: str, crud_consent_store_id: str, capsys):
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        consent_stores.create_consent_store(
            project_id, location, dataset_id, crud_consent_store_id
        )

    create()

    consent_stores.get_consent_store(
        project_id, location, dataset_id, crud_consent_store_id
    )

    consent_stores.list_consent_stores(project_id, location, dataset_id)

    consent_stores.delete_consent_store(
        project_id, location, dataset_id, crud_consent_store_id
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert "Created consent store" in out
    assert "name" in out
    assert "consentStores" in out
    assert "Deleted consent store" in out


def test_patch_consent_store(test_dataset: str, test_consent_store: str, capsys):
    consent_stores.patch_consent_store(
        project_id, location, dataset_id, consent_store_id, default_consent_ttl
    )

    out, _ = capsys.readouterr()

    assert "Patched consent store" in out


def test_get_set_consent_store_iam_policy(
    test_dataset: str, test_consent_store: str, capsys
):
    get_response = consent_stores.get_consent_store_iam_policy(
        project_id, location, dataset_id, consent_store_id
    )

    set_response = consent_stores.set_consent_store_iam_policy(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        "serviceAccount:python-docs-samples-tests@appspot.gserviceaccount.com",
        "roles/viewer",
    )

    out, _ = capsys.readouterr()

    assert "etag" in get_response
    assert "bindings" in set_response
    assert len(set_response["bindings"]) == 1
    assert "python-docs-samples-tests" in str(set_response["bindings"])
    assert "roles/viewer" in str(set_response["bindings"])
