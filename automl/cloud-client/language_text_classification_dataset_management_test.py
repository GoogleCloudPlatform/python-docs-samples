#!/usr/bin/env python

# Copyright 2019 Google LLC
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

import datetime
import os

import pytest

import language_text_classification_create_dataset
import import_dataset
import delete_dataset
import list_datasets
import get_dataset
import export_dataset

PROJECT_ID = os.environ['GCLOUD_PROJECT']
BUCKET_ID = '{}-lcm'.format(PROJECT_ID)
DATASET_ID = 'TCN2551826603472450019'


@pytest.mark.slow
def test_create_import_delete_dataset(capsys):
    # create dataset
    dataset_name = 'test_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    language_text_classification_create_dataset.create_dataset(
        PROJECT_ID, dataset_name)
    out, _ = capsys.readouterr()
    assert 'Dataset id: ' in out

    # import data
    dataset_id = out.splitlines()[1].split()[2]
    data = 'gs://{}/happiness.csv'.format(BUCKET_ID)
    import_dataset.import_dataset(PROJECT_ID, dataset_id, data)
    out, _ = capsys.readouterr()
    assert 'Data imported.' in out

    # delete dataset
    delete_dataset.delete_dataset(PROJECT_ID, dataset_id)
    out, _ = capsys.readouterr()
    assert 'Dataset deleted.' in out


def test_list_dataset(capsys):
    # list datasets
    list_datasets.list_datasets(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'Dataset id: {}'.format(DATASET_ID) in out


def test_get_dataset(capsys):
    get_dataset.get_dataset(PROJECT_ID, DATASET_ID)
    out, _ = capsys.readouterr()
    assert 'Dataset name: ' in out


def test_export_dataset(capsys):
    export_dataset.export_dataset(
        PROJECT_ID,
        DATASET_ID,
        'gs://{}/TEST_EXPORT_OUTPUT/'.format(BUCKET_ID))

    out, _ = capsys.readouterr()
    assert 'Dataset exported' in out

    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_ID)
    if len(list(bucket.list_blobs(prefix='TEST_EXPORT_OUTPUT'))) > 0:
        for blob in bucket.list_blobs(prefix='TEST_EXPORT_OUTPUT'):
            blob.delete()
