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
import time

import datasets

cloud_region = 'us-central1'
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test-dataset-{}'.format(int(time.time()))
destination_dataset_id = 'test-destination-dataset-{}'.format(int(time.time()))
keeplist_tags = 'PatientID'
time_zone = 'UTC'


def test_CRUD_dataset(capsys):
    datasets.create_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    datasets.get_dataset(
        service_account_json, project_id, cloud_region, dataset_id)

    datasets.list_datasets(
        service_account_json, project_id, cloud_region)

    # Test and also clean up
    datasets.delete_dataset(
        service_account_json, project_id, cloud_region, dataset_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert 'Created dataset' in out
    assert 'Time zone' in out
    assert 'Dataset' in out
    assert 'Deleted dataset' in out


def test_patch_dataset(capsys):
    datasets.create_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    datasets.patch_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        time_zone)

    # Clean up
    datasets.delete_dataset(
        service_account_json, project_id, cloud_region, dataset_id)

    out, _ = capsys.readouterr()

    # Check that the patch to the time zone worked
    assert 'UTC' in out


def test_deidentify_dataset(capsys):
    datasets.create_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    datasets.deidentify_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        destination_dataset_id,
        keeplist_tags)

    # Clean up
    datasets.delete_dataset(
        service_account_json, project_id, cloud_region, dataset_id)
    datasets.delete_dataset(
        service_account_json,
        project_id,
        cloud_region,
        destination_dataset_id)

    out, _ = capsys.readouterr()

    # Check that de-identify worked
    assert 'De-identified data written to' in out


def test_get_set_dataset_iam_policy(capsys):
    datasets.create_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    get_response = datasets.get_dataset_iam_policy(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    set_response = datasets.set_dataset_iam_policy(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        'serviceAccount:python-docs-samples-tests@appspot.gserviceaccount.com',
        'roles/viewer')

    # Clean up
    datasets.delete_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    out, _ = capsys.readouterr()

    assert 'etag' in get_response
    assert 'bindings' in set_response
    assert len(set_response['bindings']) == 1
    assert 'python-docs-samples-tests' in str(set_response['bindings'])
    assert 'roles/viewer' in str(set_response['bindings'])
