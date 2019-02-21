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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets')) # noqa
import datasets
import dicom_stores

cloud_region = 'us-central1'
api_key = os.environ['API_KEY']
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test_dataset-{}'.format(int(time.time()))
dicom_store_id = 'test_dicom_store_{}'.format(int(time.time()))
pubsub_topic = 'test_pubsub_topic_{}'.format(int(time.time()))

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
bucket = os.environ['CLOUD_STORAGE_BUCKET']
dcm_file_name = 'IM-0002-0001-JPEG-BASELINE.dcm'
content_uri = bucket + '/' + dcm_file_name
dcm_file = os.path.join(RESOURCES, dcm_file_name)


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


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_CRUD_dicom_store(test_dataset, capsys):
    dicom_stores.create_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    dicom_stores.get_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    dicom_stores.list_dicom_stores(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)

    dicom_stores.delete_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert 'Created DICOM store' in out
    assert 'Name' in out
    assert 'dicomStores' in out
    assert 'Deleted DICOM store' in out


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_patch_dicom_store(test_dataset, capsys):
    dicom_stores.create_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    dicom_stores.patch_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        pubsub_topic)

    # Clean up
    dicom_stores.delete_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    out, _ = capsys.readouterr()

    assert 'Patched DICOM store' in out


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_import_dicom_instance(test_dataset, capsys):
    dicom_stores.create_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    dicom_stores.import_dicom_instance(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        content_uri)

    # Clean up
    dicom_stores.delete_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    out, _ = capsys.readouterr()

    assert 'Imported DICOM instance' in out


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_export_dicom_instance(test_dataset, capsys):
    dicom_stores.create_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    dicom_stores.export_dicom_instance(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        bucket)

    # Clean up
    dicom_stores.delete_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    out, _ = capsys.readouterr()

    assert 'Exported DICOM instance' in out
