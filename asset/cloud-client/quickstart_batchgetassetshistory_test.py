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
import time

from google.cloud import storage
import pytest

import quickstart_batchgetassetshistory

PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = 'assets-{}'.format(int(time.time()))


@pytest.fixture(scope='module')
def storage_client():
    yield storage.Client()


@pytest.fixture(scope='module')
def asset_bucket(storage_client):
    bucket = storage_client.create_bucket(BUCKET)

    yield BUCKET

    try:
        bucket.delete(force=True)
    except Exception as e:
        print('Failed to delete bucket{}'.format(BUCKET))
        raise e


def test_batch_get_assets_history(asset_bucket, capsys):
    bucket_asset_name = '//storage.googleapis.com/{}'.format(BUCKET)
    asset_names = [bucket_asset_name, ]
    # There's some delay between bucket creation and when it's reflected in the
    # backend.
    time.sleep(15)
    quickstart_batchgetassetshistory.batch_get_assets_history(
        PROJECT, asset_names)
    out, _ = capsys.readouterr()

    if not out:
        if bucket_asset_name not in out:
            raise AssertionError
