# Copyright 2020 Google LLC
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

from google.cloud import storage
import pytest

import vision_async_batch_annotate_images

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
GCS_ROOT = "gs://cloud-samples-data/vision/"

BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
OUTPUT_PREFIX = f"TEST_OUTPUT_{uuid.uuid4()}"
GCS_DESTINATION_URI = f"gs://{BUCKET}/{OUTPUT_PREFIX}/"


@pytest.fixture()
def storage_client():
    yield storage.Client()


@pytest.fixture()
def bucket(storage_client):
    bucket = storage_client.get_bucket(BUCKET)

    try:
        for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
            blob.delete()
    except Exception:
        pass

    yield bucket

    for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
        blob.delete()


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_sample_asyn_batch_annotate_images(storage_client, bucket, capsys):
    input_image_uri = os.path.join(GCS_ROOT, "label/wakeupcat.jpg")

    vision_async_batch_annotate_images.sample_async_batch_annotate_images(
        input_image_uri=input_image_uri, output_uri=GCS_DESTINATION_URI
    )

    out, _ = capsys.readouterr()

    assert "Output written to GCS" in out
    assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) > 0
