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

import translate_create_dataset
import import_dataset
import delete_dataset
import list_datasets
import get_dataset
import export_dataset

project_id = os.environ['GCLOUD_PROJECT']
dataset_id = 'TRL3876092572857648864'


@pytest.mark.slow
def test_create_import_delete_dataset(capsys):
    # create dataset
    dataset_name = 'test_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    translate_create_dataset.create_dataset(project_id, dataset_name)
    out, _ = capsys.readouterr()
    assert 'Dataset id: ' in out

    # import data
    dataset_id = out.splitlines()[1].split()[2]
    data = 'gs://{}-vcm/en-ja.csv'.format(project_id)
    import_dataset.import_dataset(project_id, dataset_id, data)
    out, _ = capsys.readouterr()
    assert 'Data imported.' in out

    # delete dataset
    delete_dataset.delete_dataset(project_id, dataset_id)
    out, _ = capsys.readouterr()
    assert 'Dataset deleted.' in out


def test_list_dataset(capsys):
    # list datasets
    list_datasets.list_datasets(project_id)
    out, _ = capsys.readouterr()
    assert 'Dataset id: {}'.format(dataset_id) in out


def test_get_dataset(capsys):
    get_dataset.get_dataset(project_id, dataset_id)
    out, _ = capsys.readouterr()
    assert 'Dataset name: ' in out


def test_export_dataset(capsys):
    export_dataset.export_dataset(
        project_id,
        dataset_id,
        'gs://{}-vcm/TEST_EXPORT_OUTPUT/'.format(project_id))

    out, _ = capsys.readouterr()
    assert 'Dataset exported' in out

    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('{}-vcm'.format(project_id))
    if len(list(bucket.list_blobs(prefix='TEST_EXPORT_OUTPUT'))) > 0:
        for blob in bucket.list_blobs(prefix='TEST_EXPORT_OUTPUT'):
            blob.delete()
