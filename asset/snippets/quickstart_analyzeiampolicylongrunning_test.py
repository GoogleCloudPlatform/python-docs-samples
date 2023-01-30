#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
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

from google.cloud import bigquery
from google.cloud import storage

import pytest

import quickstart_analyzeiampolicylongrunning

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = "analysis-{}".format(int(uuid.uuid4()))
DATASET = "analysis_{}".format(int(uuid.uuid4()))


@pytest.fixture(scope="module")
def storage_client():
    yield storage.Client()


@pytest.fixture(scope="module")
def bigquery_client():
    yield bigquery.Client()


@pytest.fixture(scope="module")
def analysis_bucket(storage_client):
    bucket = storage_client.create_bucket(BUCKET)

    yield BUCKET

    try:
        bucket.delete(force=True)
    except Exception as e:
        print("Failed to delete bucket{}".format(BUCKET))
        raise e


@pytest.fixture(scope="module")
def dataset(bigquery_client):
    dataset_id = "{}.{}".format(PROJECT, DATASET)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = bigquery_client.create_dataset(dataset)

    yield DATASET

    bigquery_client.delete_dataset(
        dataset_id, delete_contents=True, not_found_ok=False)


def test_analyze_iam_policy_longrunning(analysis_bucket, dataset, capsys):
    dump_file_path = "gs://{}/analysis-dump.txt".format(analysis_bucket)
    quickstart_analyzeiampolicylongrunning.analyze_iam_policy_longrunning_gcs(PROJECT, dump_file_path)
    out, _ = capsys.readouterr()
    assert "True" in out

    dataset_id = "projects/{}/datasets/{}".format(PROJECT, dataset)
    quickstart_analyzeiampolicylongrunning.analyze_iam_policy_longrunning_bigquery(PROJECT, dataset_id, "analysis_")
    out, _ = capsys.readouterr()
    assert "True" in out
