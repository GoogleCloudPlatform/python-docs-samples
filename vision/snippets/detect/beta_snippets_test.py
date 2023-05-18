# Copyright 2018 Google LLC
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

import beta_snippets

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
GCS_ROOT = 'gs://cloud-samples-data/vision/'

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
OUTPUT_PREFIX = f'TEST_OUTPUT_{uuid.uuid4()}'
GCS_DESTINATION_URI = f'gs://{BUCKET}/{OUTPUT_PREFIX}/'


def test_localize_objects(capsys):
    path = os.path.join(RESOURCES, 'puppies.jpg')

    beta_snippets.localize_objects(path)

    out, _ = capsys.readouterr()
    assert 'Dog' in out


def test_localize_objects_uri(capsys):
    uri = GCS_ROOT + 'puppies.jpg'

    beta_snippets.localize_objects_uri(uri)

    out, _ = capsys.readouterr()
    assert 'Dog' in out


def test_handwritten_ocr(capsys):
    path = os.path.join(RESOURCES, 'handwritten.jpg')

    beta_snippets.detect_handwritten_ocr(path)

    out, _ = capsys.readouterr()
    assert 'Cloud Vision API' in out


def test_handwritten_ocr_uri(capsys):
    uri = GCS_ROOT + 'handwritten.jpg'

    beta_snippets.detect_handwritten_ocr_uri(uri)

    out, _ = capsys.readouterr()
    assert 'Cloud Vision API' in out


def test_detect_batch_annotate_files(capsys):
    file_name = os.path.join(RESOURCES, 'kafka.pdf')
    beta_snippets.detect_batch_annotate_files(file_name)
    out, _ = capsys.readouterr()
    assert 'Symbol: a' in out
    assert 'Word text: evenings' in out


def test_detect_batch_annotate_files_uri(capsys):
    gcs_uri = GCS_ROOT + 'document_understanding/kafka.pdf'
    beta_snippets.detect_batch_annotate_files_uri(gcs_uri)
    out, _ = capsys.readouterr()
    assert 'Symbol' in out
    assert 'Word text' in out


def test_async_batch_annotate_images(capsys):
    gcs_uri = GCS_ROOT + 'landmark/eiffel_tower.jpg'
    beta_snippets.async_batch_annotate_images_uri(gcs_uri, GCS_DESTINATION_URI)
    out, _ = capsys.readouterr()
    assert 'description: "Tower"' in out

    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    if len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) > 0:
        for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
            blob.delete()
