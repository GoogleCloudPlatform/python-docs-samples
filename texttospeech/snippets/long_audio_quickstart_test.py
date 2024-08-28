# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

import google.auth
from google.cloud import storage
import pytest

from long_audio_quickstart import synthesize_long_audio


@pytest.fixture(scope="module")
def test_bucket():
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"tts-long-audio-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    bucket.delete(force=True)


def test_synthesize_long_audio(capsys, test_bucket):
    file_name = "fake_file.wav"
    output_gcs_uri = f"gs://{test_bucket.name}/{file_name}"
    _, project_id = google.auth.default()
    synthesize_long_audio(project_id, output_gcs_uri)
    out, _ = capsys.readouterr()
    assert "Finished processing, check your GCS bucket to find your audio file!" in out
