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

from google.cloud import storage

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets')) # noqa
import datasets
import fhir_stores

cloud_region = 'us-central1'
api_key = os.environ['API_KEY']
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test_dataset_{}'.format(int(time.time()))
fhir_store_id = 'test_fhir_store-{}'.format(int(time.time()))
pubsub_topic = 'test_pubsub_topic-{}'.format(int(time.time()))

gcs_uri = os.environ['CLOUD_STORAGE_BUCKET']
RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
source_file_name = 'Patient.json'
resource_file = os.path.join(RESOURCES, source_file_name)
import_object = gcs_uri + '/' + source_file_name


@pytest.fixture(scope='module')
def test_dataset():
    dataset = datasets.create_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)

    yield dataset

    # Clean up
    datasets.delete_dataset(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)


@pytest.mark.skip(reason='disable until API whitelisted / enabled')
def test_CRUD_fhir_store(test_dataset, capsys):
    fhir_stores.create_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    fhir_stores.get_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    fhir_stores.list_fhir_stores(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)

    fhir_stores.delete_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert 'Created FHIR store' in out
    assert 'Name' in out
    assert 'fhirStores' in out
    assert 'Deleted FHIR store' in out


@pytest.mark.skip(reason='disable until API whitelisted / enabled')
def test_patch_fhir_store(test_dataset, capsys):
    fhir_stores.create_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    fhir_stores.patch_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        pubsub_topic)

    # Clean up
    fhir_stores.delete_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    out, _ = capsys.readouterr()

    assert 'Patched FHIR store' in out


def test_import_fhir_store_gcs(test_dataset, capsys):
    fhir_stores.create_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(gcs_uri)
    blob = bucket.blob(source_file_name)

    blob.upload_from_filename(resource_file)

    fhir_stores.import_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        import_object)

    # Clean up
    blob.delete()

    fhir_stores.delete_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    out, _ = capsys.readouterr()

    assert 'Imported FHIR resources' in out


def test_export_fhir_store_gcs(test_dataset, capsys):
    fhir_stores.create_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    fhir_stores.export_fhir_store_gcs(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id,
        gcs_uri)

    # Clean up
    fhir_stores.delete_fhir_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        fhir_store_id)

    out, _ = capsys.readouterr()

    assert 'Exported FHIR resources to bucket' in out
