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

from google.api_core import retry
import pytest

import fhir_stores  # noqa


cloud_region = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

dataset_id = f"test_dataset_{uuid.uuid4()}"
fhir_store_id = f"test_fhir_store-{uuid.uuid4()}"
test_fhir_store_id = f"test_fhir_store-{uuid.uuid4()}"

client = fhir_stores.get_client(service_account_json)


class OperationNotComplete(Exception):
    """Operation is not yet complete"""

    pass


@retry.Retry(predicate=retry.if_exception_type(OperationNotComplete))
def wait_for_operation(operation_name: str):
    operation = (
        client.projects()
        .locations()
        .datasets()
        .operations()
        .get(name=operation_name)
        .execute()
    )

    if not operation.get("done", False):
        raise OperationNotComplete(operation)


@pytest.fixture(scope="module")
def test_dataset():
    operation = fhir_stores.create_dataset(
        service_account_json, project_id, cloud_region, dataset_id
    )

    # Wait for the dataset to be created
    wait_for_operation(operation["name"])

    yield

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
    fhir_stores.create_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
    )

    fhir_stores.delete_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
    )

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert "Created FHIR store" in out
    assert "Deleted FHIR store" in out
