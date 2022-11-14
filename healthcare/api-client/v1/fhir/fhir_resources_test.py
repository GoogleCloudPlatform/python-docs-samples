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
from google.api_core import retry
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import pytest

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "datasets"))  # noqa
import datasets  # noqa
import fhir_stores  # noqa
import fhir_resources  # noqa

base_url = "https://healthcare.googleapis.com/v1"
location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

dataset_id = "test_dataset_{}".format(uuid.uuid4())
fhir_store_id = "test_fhir_store-{}".format(uuid.uuid4())
version = "R4"
resource_type = "Patient"
bundle = os.path.join(os.path.dirname(__file__), "resources/execute_bundle.json")

code_system_file = os.path.join(
    os.path.dirname(__file__), "resources/CodeSystemExample.json"
)
resource_type_from_file = "CodeSystem"
implementation_guide_file = os.path.join(
    os.path.dirname(__file__), "resources/ImplementationGuideExample.json"
)
implementation_guide_url = (
    "http://example.com/ImplementationGuide/example.implementation.guide"
)
structure_definition_file = os.path.join(
    os.path.dirname(__file__), "resources/StructureDefinitionExample.json"
)
structure_definition_profile_url_file = os.path.join(
    os.path.dirname(__file__), "resources/StructureDefinitionProfileUrlExample.json"
)
profile_url = "http://example.com/StructureDefinition/example-patient-profile-url"

BACKOFF_MAX_TIME = 750

client = discovery.build("healthcare", "v1")


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
    operation = datasets.create_dataset(project_id, location, dataset_id)

    # Wait for the dataset to be created
    wait_for_operation(operation["name"])

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=BACKOFF_MAX_TIME)
    def clean_up():
        try:
            datasets.delete_dataset(project_id, location, dataset_id)
        except HttpError as err:
            # The API returns 403 when the dataset doesn't exist.
            if err.resp.status == 404 or err.resp.status == 403:
                print("Got exception {} while deleting dataset".format(err.resp.status))
            else:
                raise

    clean_up()


@pytest.fixture(scope="module")
def test_fhir_store():
    @backoff.on_exception(backoff.expo, HttpError, max_time=BACKOFF_MAX_TIME)
    def create():
        try:
            fhir_stores.create_fhir_store(
                project_id, location, dataset_id, fhir_store_id, version
            )
        except HttpError as err:
            # We ignore 409 conflict here, because we know it's most
            # likely the first request failed on the client side, but
            # the creation suceeded on the server side.
            if err.resp.status == 409:
                print(
                    "Got exception {} while creating FHIR store".format(err.resp.status)
                )
            else:
                raise

    create()

    yield

    # Clean up
    @backoff.on_exception(backoff.expo, HttpError, max_time=BACKOFF_MAX_TIME)
    def clean_up():
        try:
            fhir_stores.delete_fhir_store(
                project_id, location, dataset_id, fhir_store_id
            )
        except HttpError as err:
            # The API returns 404 when the FHIR store doesn't exist.
            # The API returns 403 when the dataset doesn't exist, so
            # if we try to delete a FHIR store when the parent dataset
            # doesn't exist, the server will return a 403.
            if err.resp.status == 404 or err.resp.status == 403:
                print(
                    "Got exception {} while deleting FHIR store".format(err.resp.status)
                )
            else:
                raise

    clean_up()


# Fixture that creates/deletes a Patient resource for various tests.
@pytest.fixture(scope="module")
def test_patient():
    patient_response = fhir_resources.create_patient(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
    )
    patient_resource = patient_response.json()
    patient_resource_id = patient_resource["id"]

    yield patient_resource_id

    @backoff.on_exception(backoff.expo, HttpError, max_time=BACKOFF_MAX_TIME)
    # Clean up
    def clean_up():
        try:
            fhir_resources.delete_resource(
                project_id,
                location,
                dataset_id,
                fhir_store_id,
                resource_type,
                patient_resource_id,
            )

        except HttpError as err:
            # The API returns 200 whether the resource exists or was
            # successfully deleted or not.
            if err.resp.status > 200:
                print(
                    "Got exception {} while deleting FHIR store".format(err.resp.status)
                )
            else:
                raise

    clean_up()


# This test also creates a CodeSystem resource in the FHIR store, which is
# required because it serves as a reference resource to
# ImplementationGuideExample.json when calling
# test_create_implementation_guide.
def test_create_resource_from_file(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_resource_from_file(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type_from_file,
        code_system_file,
    )

    out, _ = capsys.readouterr()

    assert "Created FHIR resource" in out


def test_create_patient(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_patient(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
    )

    out, _ = capsys.readouterr()

    assert "Created Patient" in out


def test_validate_resource(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.validate_resource(
        project_id, location, dataset_id, fhir_store_id, resource_type
    )

    out, _ = capsys.readouterr()

    # Should succeed because we are validating a standard Patient resource
    # against the base FHIR store profile without any customization
    assert '{"text": "success"}' in out


def test_validate_resource_profile_url(
    test_dataset, test_fhir_store, test_patient, capsys
):
    # Create a StructureDefinition resource that only exists in the FHIR store
    # to ensure that the validate_resource_profile_url method fails, because the
    # validation does not adhere to the constraints in the StructureDefinition.
    fhir_resources.create_structure_definition(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        structure_definition_profile_url_file,
    )

    fhir_resources.validate_resource_profile_url(
        project_id, location, dataset_id, fhir_store_id, resource_type, profile_url
    )

    out, _ = capsys.readouterr()

    # Should fail because we are purposefully validating a resource against a
    # profile that it does not match
    assert '"severity": "error"' in out


def test_get_patient(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.get_resource(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
    )

    out, _ = capsys.readouterr()

    assert "Got Patient resource" in out


def test_update_patient(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.update_resource(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
    )

    out, _ = capsys.readouterr()

    assert "Updated Patient resource" in out


def test_resource_versions(test_dataset, test_fhir_store, test_patient, capsys):
    # We have to update the resource so that different versions of it are
    # created, then we test to see if we can get/delete those versions.
    fhir_resources.update_resource(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
    )

    history = fhir_resources.list_resource_history(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
    )

    fhir_resources.get_resource_history(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
        history["entry"][-1]["resource"]["meta"]["versionId"],
    )

    out, _ = capsys.readouterr()

    # list_resource_history test
    assert "History for Patient resource" in out
    # get_resource_history test
    assert "Got history for Patient resource" in out


def test_search_resources_post(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.search_resources_post(
        project_id, location, dataset_id, fhir_store_id
    )

    out, _ = capsys.readouterr()

    assert "Using POST request" in out


def test_execute_bundle(test_dataset, test_fhir_store, capsys):
    fhir_resources.execute_bundle(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        bundle,
    )

    out, _ = capsys.readouterr()

    assert "Executed bundle from file" in out


def test_create_structure_definition(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_structure_definition(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        structure_definition_file,
    )

    out, _ = capsys.readouterr()

    assert "Created StructureDefinition resource" in out


def test_create_implementation_guide(test_dataset, test_fhir_store, capsys):
    fhir_resources.create_implementation_guide(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        implementation_guide_file,
    )

    out, _ = capsys.readouterr()

    assert "Created ImplementationGuide resource" in out


def test_enable_implementation_guide(test_dataset, test_fhir_store, capsys):
    fhir_resources.enable_implementation_guide(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        implementation_guide_url,
    )

    out, _ = capsys.readouterr()

    assert "Enabled ImplementationGuide" in out


def test_delete_patient(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.delete_resource(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient,
    )

    out, _ = capsys.readouterr()

    assert "Deleted Patient resource" in out
