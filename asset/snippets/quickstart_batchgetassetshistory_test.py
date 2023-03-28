#!/usr/bin/env python

# Copyright 2018 Google LLC.
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

from google.api_core.retry import Retry
from google.api_core.exceptions import InvalidArgument
from google.cloud import storage
import pytest

import quickstart_batchgetassetshistory

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = "assets-{}".format(uuid.uuid4().hex)


@pytest.fixture(scope="module")
def storage_client():
    yield storage.Client(project=PROJECT)


@pytest.fixture(scope="module")
def asset_bucket(storage_client):
    bucket = storage_client.create_bucket(BUCKET, project=PROJECT)

    yield BUCKET

    try:
        bucket.delete(force=True)
    except Exception as e:
        print("Failed to delete bucket{}".format(BUCKET))
        raise e


def test_batch_get_assets_history(asset_bucket, capsys):
    bucket_asset_name = "//storage.googleapis.com/{}".format(BUCKET)
    asset_names = [
        bucket_asset_name,
    ]

    @Retry(on_error=InvalidArgument, timeout=60)
    def eventually_consistent_test():
        quickstart_batchgetassetshistory.batch_get_assets_history(PROJECT, asset_names)
        out, _ = capsys.readouterr()

        assert bucket_asset_name in out

    eventually_consistent_test()
