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
import re
import sys
import time

# Add datasets for bootstrapping datasets for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets')) # noqa
import datasets
import hl7v2_stores
import hl7v2_messages

cloud_region = 'us-central1'
project_id = os.environ['GOOGLE_CLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

dataset_id = 'test_dataset_{}'.format(int(time.time()))
hl7v2_store_id = 'test_hl7v2_store-{}'.format(int(time.time()))
hl7v2_message_file = 'resources/hl7-sample-ingest.json'
label_key = 'PROCESSED'
label_value = 'TRUE'


@pytest.fixture(scope='module')
def test_dataset():
    dataset = datasets.create_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)

    yield dataset

    # Clean up
    datasets.delete_dataset(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id)


@pytest.fixture(scope='module')
def test_hl7v2_store():
    hl7v2_store = hl7v2_stores.create_hl7v2_store(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    yield hl7v2_store

    hl7v2_stores.delete_hl7v2_store(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)


def test_CRUD_hl7v2_message(test_dataset, test_hl7v2_store, capsys):
    hl7v2_messages.create_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_file)

    hl7v2_messages_list = hl7v2_messages.list_hl7v2_messages(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    hl7v2_messages_list_to_str = str(hl7v2_messages_list).split('/', 9)[9]
    hl7v2_message_id = re.sub('\']', '', hl7v2_messages_list_to_str)

    hl7v2_messages.get_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id)

    hl7v2_messages.delete_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert 'Created HL7v2 message' in out
    assert 'Name' in out
    assert 'Deleted HL7v2 message' in out


def test_ingest_hl7v2_message(test_dataset, test_hl7v2_store, capsys):
    hl7v2_messages.ingest_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_file)

    hl7v2_messages_list = hl7v2_messages.list_hl7v2_messages(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    hl7v2_messages_list_to_str = str(hl7v2_messages_list).split('/', 9)[9]
    hl7v2_message_id = re.sub('\']', '', hl7v2_messages_list_to_str)

    hl7v2_messages.get_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id)

    hl7v2_messages.delete_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id)

    out, _ = capsys.readouterr()

    # Check that ingest/get/list/delete worked
    assert 'Ingested HL7v2 message' in out
    assert 'Name' in out
    assert 'Deleted HL7v2 message' in out


def test_patch_hl7v2_message(test_dataset, test_hl7v2_store, capsys):
    hl7v2_messages.create_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_file)

    hl7v2_messages_list = hl7v2_messages.list_hl7v2_messages(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id)

    hl7v2_messages_list_to_str = str(hl7v2_messages_list).split('/', 9)[9]
    hl7v2_message_id = re.sub('\']', '', hl7v2_messages_list_to_str)

    hl7v2_messages.patch_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id,
        label_key,
        label_value)

    hl7v2_messages.delete_hl7v2_message(
        service_account_json,
        project_id,
        cloud_region,
        dataset_id,
        hl7v2_store_id,
        hl7v2_message_id)

    out, _ = capsys.readouterr()

    # Check that patch worked
    assert 'Patched HL7v2 message' in out
