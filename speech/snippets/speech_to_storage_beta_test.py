# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from google.api_core.retry import Retry
from google.cloud import storage
import pytest

import speech_to_storage_beta


storage_client = storage.Client()

BUCKET_UUID = str(uuid.uuid4())[:8]
BUCKET_NAME = f"speech-{BUCKET_UUID}"
BUCKET_PREFIX = "export-transcript-output-test"

INPUT_STORAGE_URI = "gs://cloud-samples-data/speech/commercial_mono.wav"
language_code = "en-US"


@Retry()
def test_export_transcript_to_storage_beta(
    bucket: storage.Bucket, capsys: pytest.CaptureFixture
) -> None:
    results = speech_to_storage_beta.export_transcript_to_storage_beta(
        INPUT_STORAGE_URI,
        BUCKET_NAME,
        BUCKET_PREFIX,
    )
    assert len(results) > 0


@pytest.fixture
def bucket() -> storage.Bucket:
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket = storage_client.bucket(BUCKET_NAME)
    bucket.storage_class = "COLDLINE"
    storage_client.create_bucket(bucket, location="us")
    yield bucket

    blobs = storage_client.list_blobs(BUCKET_NAME, prefix=BUCKET_PREFIX)

    for blob in blobs:
        blob.delete()

    bucket.delete(force=True)
