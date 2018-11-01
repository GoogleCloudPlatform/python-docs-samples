# Copyright 2016 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest
import requests

import list_gcs_buckets

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
ACCESS_KEY_ID = os.environ['CLOUD_STORAGE_ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['CLOUD_STORAGE_SECRET_ACCESS_KEY']

def test_list_blobs(capsys):
    list_gcs_buckets.list_blobs(google_access_key_id=ACCESS_KEY_ID,
        google_secret_access_key=SECRET_ACCESS_KEY)
    out, _ = capsys.readouterr()
    assert BUCKET in out
