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

from google.cloud import storage

from detect_pdf import async_detect_document

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
OUTPUT_PREFIX = 'OCR_PDF_TEST_OUTPUT'
GCS_SOURCE_URI = 'gs://{}/HodgeConj.pdf'.format(BUCKET)
GCS_DESTINATION_URI = 'gs://{}/{}/'.format(BUCKET, OUTPUT_PREFIX)


def test_async_detect_document(capsys):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) == 0

    async_detect_document(
        gcs_source_uri=GCS_SOURCE_URI,
        gcs_destination_uri=GCS_DESTINATION_URI)
    out, _ = capsys.readouterr()

    assert 'Hodge conjecture' in out
    assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) == 3

    for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
        blob.delete()
