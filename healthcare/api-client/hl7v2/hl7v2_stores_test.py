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
import hl7v2_stores

cloud_region = 'us-central1'
api_key = os.environ['API_KEY']
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test_dataset_{}'.format(int(time.time()))
hl7v2_store_id = 'test_hl7v2_store-{}'.format(int(time.time()))
pubsub_topic = 'test_pubsub_topic-{}'.format(int(time.time()))


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
def test_CRUD_hl7v2_store(test_dataset, capsys):
    hl7v2_stores.create_hl7v2_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    hl7v2_stores.get_hl7v2_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    hl7v2_stores.list_hl7v2_stores(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id)

    hl7v2_stores.delete_hl7v2_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert 'Created HL7v2 store' in out
    assert 'Name' in out
    assert 'hl7V2Stores' in out
    assert 'Deleted HL7v2 store' in out


@pytest.mark.skip(reason='disable until have access to healthcare api')
def test_patch_hl7v2_store(test_dataset, capsys):
    hl7v2_stores.create_hl7v2_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    hl7v2_stores.patch_hl7v2_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        pubsub_topic)

    # Clean up
    hl7v2_stores.delete_hl7v2_store(
        service_account_json,
        api_key,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    out, _ = capsys.readouterr()

    assert 'Patched HL7v2 store' in out
