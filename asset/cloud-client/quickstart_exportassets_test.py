#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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

from google.cloud import pubsub_v1
import pytest
import quickstart

PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = 'bucket-for-assets'

@pytest.fixture(scope='module')
def storage_client():
  yield storage.Client()


@pytest.fixture(scope='module')
def asset_bucket(storage_client):
    topic_path = storage_client.create_bucket(BUCKET)

    try:
        stroage_client.delete_bucket(BUCKET)
    except Exception:
        pass

    yield BUCKET

def test_export_assets(asset_bucket):

    dump_file_path = "gs://", asset_bucket, "/assets-dump.txt"
    quickstart.end_to_end(PROJECT, dump_file_path)
    out, _ = capsys.readouterr()

    assert "uri: \"gs://cai-prober-prod-for-assets/phython-test.txt\"" in out
