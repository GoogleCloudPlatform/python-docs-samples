# Copyright 2019 Google, Inc.
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

import list_gcs_buckets

BUCKET = os.environ["GOOGLE_CLOUD_PROJECT_S3_SDK"]
KEY_ID = os.environ["STORAGE_HMAC_ACCESS_KEY_ID"]
SECRET_KEY = os.environ["STORAGE_HMAC_ACCESS_SECRET_KEY"]


def test_list_blobs(capsys):
    list_gcs_buckets.list_gcs_buckets(
        google_access_key_id=KEY_ID, google_access_key_secret=SECRET_KEY
    )
    out, _ = capsys.readouterr()
    assert BUCKET in out
