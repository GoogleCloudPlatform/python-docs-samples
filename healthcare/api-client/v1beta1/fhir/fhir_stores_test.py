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

import backoff
import pytest
from requests.exceptions import HTTPError

import fhir_stores  # noqa


cloud_region = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

dataset_id = "test_dataset_{}".format(uuid.uuid4())
fhir_store_id = "test_fhir_store-{}".format(uuid.uuid4())
test_fhir_store_id = "test_fhir_store-{}".format(uuid.uuid4())


BACKOFF_MAX_TIME = 500


@pytest.fixture(scope="module")
def test_dataset():
    dataset = fhir_stores.create_dataset(
        service_account_json, project_id, cloud_region, dataset_id
    )

    yield dataset

    # Clean up
    fhir_stores.delete_dataset(
        service_account_json, project_id, cloud_region, dataset_id
    )


@pytest.fixture(scope="module")
def test_fhir_store():
    resp = fhir_stores.create_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, test_fhir_store_id
    )

    yield resp

    fhir_stores.delete_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, test_fhir_store_id
    )


def test_create_delete_fhir_store(test_dataset, capsys):
    # We see HttpErrors with "dataset not initialized" message.
    # I think retry will mitigate the flake.
    @backoff.on_exception(backoff.expo, HTTPError, max_time=BACKOFF_MAX_TIME)
    def create():
        fhir_stores.create_fhir_store(
            service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
        )
    create()

    fhir_stores.delete_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert "Created FHIR store" in out
    assert "Deleted FHIR store" in out
