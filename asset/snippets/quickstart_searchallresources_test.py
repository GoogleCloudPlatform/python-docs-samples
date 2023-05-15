#!/usr/bin/env python

# Copyright 2020 Google LLC.
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

import backoff
from google.api_core.exceptions import NotFound
from google.cloud import bigquery
import pytest

import quickstart_searchallresources

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
DATASET = f"dataset_{uuid.uuid4().hex}"


@pytest.fixture(scope="module")
def bigquery_client():
    yield bigquery.Client()


@pytest.fixture(scope="module")
def asset_dataset(bigquery_client):
    dataset = bigquery_client.create_dataset(DATASET)

    yield DATASET

    try:
        bigquery_client.delete_dataset(dataset)
    except NotFound as e:
        print(f"Failed to delete dataset {DATASET}")
        raise e


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_search_all_resources(asset_dataset, capsys):
    scope = f"projects/{PROJECT}"
    query = f"name:{DATASET}"

    # Dataset creation takes some time to propagate, so the dataset is not
    # immediately searchable. Need some time before the snippet will pass.
    @backoff.on_exception(backoff.expo, (AssertionError), max_time=240)
    def eventually_consistent_test():
        quickstart_searchallresources.search_all_resources(scope, query=query)
        out, _ = capsys.readouterr()

        assert DATASET in out

    eventually_consistent_test()
