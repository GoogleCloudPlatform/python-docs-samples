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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))  # noqa
import datasets
import dicom_stores
import dicomweb

cloud_region = 'us-central1'
api_key = os.environ['API_KEY']
base_url = 'https://healthcare.googleapis.com/v1alpha'
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test_dataset-{}'.format(int(time.time()))
dicom_store_id = 'test_dicom_store_{}'.format(int(time.time()))

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
dcm_file_name = 'IM-0002-0001-JPEG-BASELINE.dcm'
dcm_file = os.path.join(RESOURCES, dcm_file_name)
# The study_uid is not assigned by the server and is part of the
# metadata of dcm_file
study_uid = '1.2.840.113619.2.176.3596.3364818.7819.1259708454.105'


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


@pytest.fixture(scope='module')
def test_dicom_store():
    dicom_store = dicom_stores.create_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    yield dicom_store

    # Clean up
    dicom_stores.delete_dicom_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_dicomweb_store_instance(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        dcm_file)

    out, _ = capsys.readouterr()

    # Check that store instance worked
    assert 'Stored DICOM instance' in out

    dicomweb.dicomweb_delete_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid)


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_dicomweb_search_instance(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        dcm_file)

    dicomweb.dicomweb_search_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id)

    out, _ = capsys.readouterr()

    # Check that store instance worked
    assert 'Instances:' in out

    dicomweb.dicomweb_delete_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid)


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_dicomweb_retrieve_study(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        dcm_file)

    dicomweb.dicomweb_retrieve_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid)

    out, _ = capsys.readouterr()

    # Check that store instance worked
    assert 'Retrieved study with UID:' in out

    dicomweb.dicomweb_delete_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid)


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_dicomweb_delete_study(test_dataset, test_dicom_store, capsys):
    dicomweb.dicomweb_store_instance(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        dcm_file)

    dicomweb.dicomweb_delete_study(
        service_account_json,
        base_url,
        project_id,
        cloud_region,
        dataset_id,
        dicom_store_id,
        study_uid)

    out, _ = capsys.readouterr()

    # Check that store instance worked
    assert 'Deleted study.' in out
