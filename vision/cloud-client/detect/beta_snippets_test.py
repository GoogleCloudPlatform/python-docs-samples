# Copyright 2018 Google LLC All Rights Reserved.
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

import beta_snippets

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
GCS_ROOT = 'gs://cloud-samples-data/vision/'


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


def test_detect_pdf_document(capsys):
    file_name = os.path.join(RESOURCES, 'kafka.pdf')
    beta_snippets.detect_document_features(file_name)
    out, _ = capsys.readouterr()
    assert 'Symbol: a' in out
    assert 'Word text: evenings' in out


def test_detect_pdf_document_from_gcs(capsys):
    gcs_uri = GCS_ROOT + 'document_understanding/kafka.pdf'
    beta_snippets.detect_document_features_uri(gcs_uri)
    out, _ = capsys.readouterr()
    assert 'Symbol' in out
    assert 'Word text' in out
