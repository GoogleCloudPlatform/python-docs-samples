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
from google.api_core import retry
import pytest
from requests.exceptions import HTTPError

import fhir_stores  # noqa
import fhir_resources  # noqa


cloud_region = "us-central1"
base_url = "https://healthcare.googleapis.com/v1beta1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

dataset_id = f"test_dataset_{uuid.uuid4()}"
fhir_store_id = f"test_fhir_store-{uuid.uuid4()}"
resource_type = "Patient"
client = fhir_stores.get_client(service_account_json)

BACKOFF_MAX_TIME = 750


# A giveup callback for backoff.
def fatal_code(e):
    return 400 <= e.response.status_code < 500


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
    fhir_store = fhir_stores.create_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
    )

    yield fhir_store

    # Clean up
    fhir_stores.delete_fhir_store(
        service_account_json, project_id, cloud_region, dataset_id, fhir_store_id
    )


# Fixture that creates/deletes a Patient resource for various tests.
@pytest.fixture(scope="module")
def test_patient():
    patient_response = fhir_resources.create_patient(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
    )
    patient_resource_id = patient_response.json()["id"]

    yield patient_resource_id

    # Clean up
    fhir_resources.delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        patient_resource_id,
    )


def test_create_patient(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_patient(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
    )

    out, _ = capsys.readouterr()

    print(out)

    assert "Created Patient" in out


@pytest.mark.skip(reason="flaky test sometimes returns 403 errors, need to investigate")
def test_conditional_patch_resource(
    test_dataset, test_fhir_store, test_patient, capsys
):
    # The conditional method tests use an Observation, so we have to create an
    # Encounter from test_patient and then create an Observation from the
    # Encounter.
    encounter_response = fhir_resources.create_encounter(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        test_patient,
    )

    encounter_resource_id = encounter_response.json()["id"]

    observation_response = fhir_resources.create_observation(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        test_patient,
        encounter_resource_id,
    )

    observation_resource_id = observation_response.json()["id"]

    fhir_resources.conditional_patch_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
    )

    # In accordance with the FHIR spec, if conditional patch or conditional update
    # can only be applied to one resource at a time. If the search criteria
    # identify more than one match, the request returns a 412 Precondition Failed
    # error. Every time the tests create an Observation resource, the resource is
    # identical, therefore you have to delete each Observation after it's created
    # or else conditional patch/update will detect more than one Observation
    # that matches.
    fhir_resources.delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        "Observation",
        observation_resource_id,
    )

    out, _ = capsys.readouterr()

    print(out)

    assert "Conditionally patched" in out


@pytest.mark.skip(reason="flaky test sometimes returns 412 errors, need to investigate")
def test_conditional_update_resource(
    test_dataset, test_fhir_store, test_patient, capsys
):
    # The conditional method tests use an Observation, so we have to create an
    # Encounter from test_patient and then create an Observation from the
    # Encounter.
    encounter_response = fhir_resources.create_encounter(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        test_patient,
    )

    encounter_resource_id = encounter_response.json()["id"]

    observation_response = fhir_resources.create_observation(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        test_patient,
        encounter_resource_id,
    )

    observation_resource_id = observation_response.json()["id"]

    fhir_resources.conditional_update_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        test_patient,
        encounter_resource_id,
    )

    # In accordance with the FHIR spec, if conditional patch or conditional update
    # can only be applied to one resource at a time. If the search criteria
    # identify more than one match, the request returns a 412 Precondition Failed
    # error. Every time the tests create an Observation resource, the resource is
    # identical, therefore you have to delete each Observation after it's created
    # or else conditional patch/update will detect more than one Observation
    # that matches.
    fhir_resources.delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        "Observation",
        observation_resource_id,
    )

    out, _ = capsys.readouterr()

    assert "Conditionally updated" in out


def test_conditional_delete_resource(
    test_dataset, test_fhir_store, test_patient, capsys
):
    # The conditional method tests use an Observation, so we have to create an
    # Encounter from test_patient and then create an Observation from the
    # Encounter.
    @backoff.on_exception(
        backoff.expo, HTTPError, max_time=BACKOFF_MAX_TIME, giveup=fatal_code
    )
    def create_encounter():
        encounter_response = fhir_resources.create_encounter(
            service_account_json,
            base_url,
            project_id,
            cloud_region,
            dataset_id,
            fhir_store_id,
            test_patient,
        )
        return encounter_response.json()["id"]

    encounter_resource_id = create_encounter()

    @backoff.on_exception(
        backoff.expo, HTTPError, max_time=BACKOFF_MAX_TIME, giveup=fatal_code
    )
    def create_observation():
        fhir_resources.create_observation(
            service_account_json,
            base_url,
            project_id,
            cloud_region,
            dataset_id,
            fhir_store_id,
            test_patient,
            encounter_resource_id,
        )

    create_observation()

    @backoff.on_exception(
        backoff.expo, HTTPError, max_time=BACKOFF_MAX_TIME, giveup=fatal_code
    )
    def conditional_delete_resource():
        fhir_resources.conditional_delete_resource(
            service_account_json,
            base_url,
            project_id,
            cloud_region,
            dataset_id,
            fhir_store_id,
        )

    conditional_delete_resource()
    out, _ = capsys.readouterr()
    print(out)
    assert "Conditionally deleted" in out


def test_delete_patient(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
    )

    out, _ = capsys.readouterr()

    print(out)

    assert "Deleted Patient resource" in out
