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

from google.cloud import storage

import export_dataset

PROJECT_ID = 'cdpe-automl-tests'
BUCKET_ID = "{}-lcm".format(PROJECT_ID)
DATASET_ID = "TEN6765176298449928192"
PREFIX = "TEST_EXPORT_OUTPUT_" + datetime.datetime.now().strftime(
    "%Y%m%d%H%M%S"
)


def test_export_dataset(capsys):
    export_dataset.export_dataset(
        PROJECT_ID, DATASET_ID, "gs://{}/{}/".format(BUCKET_ID, PREFIX)
    )

    out, _ = capsys.readouterr()
    assert "Dataset exported" in out

    # Delete the created files
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_ID)
    if len(list(bucket.list_blobs(prefix=PREFIX))) > 0:
        for blob in bucket.list_blobs(prefix=PREFIX):
            blob.delete()
