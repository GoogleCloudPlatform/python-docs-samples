# Copyright 2019 Google LLC All Rights Reserved.
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

import pytest

from google.cloud import storage
from parse_table import parse_table_gcs


PROJECT_ID = os.getenv('GCLOUD_PROJECT')
GCS_SOURCE_URI = 'gs://cloud-samples-data/documentai/fake_invoice.pdf'
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@pytest.fixture
def gcs_destination_uri():
    prefix = uuid.uuid4()
    uri = 'gs://{}/{}/'.format(BUCKET, prefix)

    yield uri

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    for blob in bucket.list_blobs(prefix=prefix):
        blob.delete()


def test_parse_table_gcs(capsys, gcs_destination_uri):
    parse_table_gcs(PROJECT_ID, GCS_SOURCE_URI, gcs_destination_uri)

    out, _ = capsys.readouterr()
    assert 'Misc processing fees' in out
