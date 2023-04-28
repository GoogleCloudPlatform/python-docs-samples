#!/usr/bin/env python

# Copyright 2018 Google LLC. All Rights Reserved.
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
import uuid

from google.cloud import asset_v1
from google.cloud import bigquery
from google.cloud import storage
import pytest

import quickstart_exportassets

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = "assets-{}".format(uuid.uuid4().hex)
DATASET = "assets_{}".format(int(uuid.uuid4()))


@pytest.fixture(scope="module")
def storage_client():
    yield storage.Client()


@pytest.fixture(scope="module")
def bigquery_client():
    yield bigquery.Client()


@pytest.fixture(scope="module")
def asset_bucket(storage_client):
    bucket = storage_client.create_bucket(BUCKET)

    yield BUCKET

    try:
        bucket.delete(force=True)
    except Exception as e:
        print("Failed to delete bucket{}".format(BUCKET))
        raise e


@pytest.fixture(scope='module')
def dataset(bigquery_client):
    dataset_id = "{}.{}".format(PROJECT, DATASET)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = bigquery_client.create_dataset(dataset)

    yield DATASET

    bigquery_client.delete_dataset(
            dataset_id, delete_contents=True, not_found_ok=False)


def test_export_assets(asset_bucket, dataset, capsys):
    content_type = asset_v1.ContentType.IAM_POLICY
    dump_file_path = "gs://{}/assets-dump.txt".format(asset_bucket)
    quickstart_exportassets.export_assets(
        PROJECT,
        dump_file_path,
        content_type=content_type
    )
    out, _ = capsys.readouterr()
    assert dump_file_path in out

    content_type = asset_v1.ContentType.RESOURCE
    dataset_id = "projects/{}/datasets/{}".format(PROJECT, dataset)
    quickstart_exportassets.export_assets_bigquery(
        PROJECT, dataset_id, "assettable", content_type)
    out, _ = capsys.readouterr()
    assert dataset_id in out

    content_type_r = asset_v1.ContentType.RELATIONSHIP
    quickstart_exportassets.export_assets_bigquery(
        PROJECT, dataset_id, "assettable", content_type_r)
    out_r, _ = capsys.readouterr()
    assert dataset_id in out_r
