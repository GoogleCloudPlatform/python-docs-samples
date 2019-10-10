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
import pytest
import sys
import time

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..',
                             'datasets'))  # noqa
import datasets
import fhir_stores
import fhir_resources

cloud_region = 'us-central1'
base_url = 'https://healthcare.googleapis.com/v1beta1'
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

bundle = os.path.join(
    os.path.dirname(__file__),
    'resources/execute_bundle.json')
dataset_id = 'test_dataset_{}'.format(int(time.time()))
fhir_store_id = 'test_fhir_store-{}'.format(int(time.time()))
resource_type = 'Patient'


@pytest.fixture(scope='module')
def test_dataset():
    dataset = datasets.create_dataset(service_account_json, project_id,
                                      cloud_region, dataset_id)

    yield dataset

    # Clean up
    datasets.delete_dataset(service_account_json, project_id, cloud_region,
                            dataset_id)


@pytest.fixture(scope='module')
def test_fhir_store():
    fhir_store = fhir_stores.create_fhir_store(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    yield fhir_store

    # Clean up
    fhir_stores.delete_fhir_store(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

# Fixture that creates/deletes a Patient resource for various tests.
@pytest.fixture(scope='module')
def test_patient():
    patient_response = fhir_resources.create_patient(service_account_json,
                                                     base_url, project_id,
                                                     cloud_region, dataset_id,
                                                     fhir_store_id)
    patient_resource_id = patient_response.json()['id']

    yield patient_resource_id

    # Clean up
    fhir_resources.delete_resource(service_account_json, base_url, project_id,
                                   cloud_region, dataset_id, fhir_store_id,
                                   resource_type, patient_resource_id)


def test_CRUD_patient(test_dataset, test_fhir_store, capsys):
    # Manually create a new Patient here to test that creating a Patient
    # works.
    patient_response = fhir_resources.create_patient(service_account_json,
                                                     base_url, project_id,
                                                     cloud_region, dataset_id,
                                                     fhir_store_id)

    # Save the patient_resource_id because it's how you identify the Patient
    patient_resource_id = patient_response.json()['id']

    fhir_resources.get_resource(service_account_json, base_url, project_id,
                                cloud_region, dataset_id, fhir_store_id,
                                resource_type, patient_resource_id)

    fhir_resources.update_resource(service_account_json, base_url, project_id,
                                   cloud_region, dataset_id, fhir_store_id,
                                   resource_type, patient_resource_id)

    fhir_resources.patch_resource(service_account_json, base_url, project_id,
                                  cloud_region, dataset_id, fhir_store_id,
                                  resource_type, patient_resource_id)

    fhir_resources.delete_resource(service_account_json, base_url, project_id,
                                   cloud_region, dataset_id, fhir_store_id,
                                   resource_type, patient_resource_id)

    out, _ = capsys.readouterr()

    print(out)

    # create_patient test
    assert 'Created Patient' in out
    # get_resource test
    assert 'Got Patient resource' in out
    # update_resource test
    assert 'Updated Patient resource' in out
    # patch_resource test
    assert 'Patched Patient resource' in out
    # delete_resource test
    assert 'Deleted Patient resource' in out


def test_resource_versions(
        test_dataset,
        test_fhir_store,
        test_patient,
        capsys):
    # We have to update the resource so that different versions of it are
    # created, then we test to see if we can get/delete those versions.
    fhir_resources.update_resource(service_account_json, base_url, project_id,
                                   cloud_region, dataset_id, fhir_store_id,
                                   resource_type, test_patient)

    history = fhir_resources.list_resource_history(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        resource_type,
        test_patient)

    fhir_resources.get_resource_history(
        service_account_json, base_url, project_id, cloud_region, dataset_id,
        fhir_store_id, resource_type, test_patient,
        history['entry'][-1]['resource']['meta']['versionId'])

    fhir_resources.delete_resource_purge(service_account_json, base_url,
                                         project_id, cloud_region, dataset_id,
                                         fhir_store_id, resource_type,
                                         test_patient)

    out, _ = capsys.readouterr()

    print(out)

    # list_resource_history test
    assert 'History for Patient resource' in out
    # get_resource_history test
    assert 'Got history for Patient resource' in out
    # delete_resource_purge test
    assert 'Deleted versions of Patient resource' in out


def test_conditions_resource(
        test_dataset,
        test_fhir_store,
        test_patient,
        capsys):
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
        test_patient)

    encounter_resource_id = encounter_response.json()['id']

    fhir_resources.create_observation(
        service_account_json, base_url, project_id, cloud_region, dataset_id,
        fhir_store_id, test_patient, encounter_resource_id)

    fhir_resources.conditional_patch_resource(service_account_json, base_url,
                                              project_id, cloud_region,
                                              dataset_id, fhir_store_id)

    fhir_resources.conditional_update_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        test_patient,
        encounter_resource_id)

    fhir_resources.conditional_delete_resource(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    out, _ = capsys.readouterr()

    print(out)
    # conditional_patch_resource test
    assert 'Conditionally patched' in out
    # conditional_update_resource test
    assert 'Conditionally updated' in out
    # conditional_delete_resource test
    assert 'Conditionally deleted' in out


def test_search_resources(test_dataset, test_fhir_store, test_patient, capsys):
    fhir_resources.search_resources_get(service_account_json, base_url,
                                        project_id, cloud_region, dataset_id,
                                        fhir_store_id, resource_type)

    fhir_resources.search_resources_post(service_account_json, base_url,
                                         project_id, cloud_region, dataset_id,
                                         fhir_store_id)

    out, _ = capsys.readouterr()

    # search_resources_get test
    assert 'Using GET request' in out
    # search_resources_post test
    assert 'Using POST request' in out


def test_get_patient_everything(
        test_dataset,
        test_fhir_store,
        test_patient,
        capsys):
    fhir_resources.get_patient_everything(service_account_json, base_url,
                                          project_id, cloud_region, dataset_id,
                                          fhir_store_id, test_patient)

    out, _ = capsys.readouterr()

    # get_patient_everything test
    assert 'id' in out


def test_get_metadata(test_dataset, test_fhir_store, capsys):
    fhir_resources.get_metadata(service_account_json, base_url, project_id,
                                cloud_region, dataset_id, fhir_store_id)

    out, _ = capsys.readouterr()

    # get_metadata test
    assert 'fhirVersion' in out


def test_execute_bundle(test_dataset, test_fhir_store, capsys):
    fhir_resources.execute_bundle(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        bundle)

    out, _ = capsys.readouterr()

    # execute_bundle test
    assert 'Executed bundle' in out
