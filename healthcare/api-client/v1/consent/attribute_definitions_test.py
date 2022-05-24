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
import attribute_definitions  # noqa

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

dataset_id = "test-dataset-{}".format(uuid.uuid4())
consent_store_id = "test-consent-store-{}".format(uuid.uuid4())
resource_attribute_definition_id = "test_resource_attribute_definition_id_{}".format(
    uuid.uuid4().hex[:5]
)
request_attribute_definition_id = "test_request_attribute_definition_id_{}".format(
    uuid.uuid4().hex[:5]
)

description = "whether the data is de-identifiable"


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
                print("Got exception {} while creating dataset".format(err.resp.status))
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
                print("Got exception {} while deleting dataset".format(err.resp.status))
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


def test_CRUD_resource_attribute_definition(
    test_dataset: str, test_consent_store: str, capsys
):
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        attribute_definitions.create_resource_attribute_definition(
            project_id,
            location,
            dataset_id,
            consent_store_id,
            resource_attribute_definition_id,
        )

    create()

    attribute_definitions.get_attribute_definition(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        resource_attribute_definition_id,
    )

    attribute_definitions.list_attribute_definitions(
        project_id, location, dataset_id, consent_store_id
    )

    attribute_definitions.patch_attribute_definition(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        resource_attribute_definition_id,
        description,
    )

    attribute_definitions.delete_attribute_definition(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        resource_attribute_definition_id,
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/patch/delete worked
    assert "Created RESOURCE attribute definition" in out
    assert "Got attribute definition" in out
    assert "name" in out
    assert "Patched attribute definition" in out
    assert "Deleted attribute definition" in out


def test_CRUD_request_attribute_definition(
    test_dataset: str, test_consent_store: str, capsys
):
    @backoff.on_exception(backoff.expo, HttpError, max_time=60)
    def create():
        attribute_definitions.create_request_attribute_definition(
            project_id,
            location,
            dataset_id,
            consent_store_id,
            request_attribute_definition_id,
        )

    create()

    attribute_definitions.get_attribute_definition(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        request_attribute_definition_id,
    )

    attribute_definitions.list_attribute_definitions(
        project_id, location, dataset_id, consent_store_id
    )

    attribute_definitions.patch_attribute_definition(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        request_attribute_definition_id,
        description,
    )

    attribute_definitions.delete_attribute_definition(
        project_id,
        location,
        dataset_id,
        consent_store_id,
        request_attribute_definition_id,
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/patch/delete worked
    assert "Created REQUEST attribute definition" in out
    assert "Got attribute definition" in out
    assert "name" in out
    assert "Patched attribute definition" in out
    assert "Deleted attribute definition" in out
