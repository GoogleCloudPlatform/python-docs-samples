# Copyright 2019 Google LLC
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
import translate_create_glossary
import translate_delete_glossary
import uuid

PROJECT_ID = os.environ['GCLOUD_PROJECT']
MODEL_ID = os.environ['AUTOML_TRANSLATION_MODEL_ID']
GLOSSARY_INPUT_URI = 'gs://cloud-samples-data/translation/glossary.csv'

@pytest.fixture(scope='function')
def unique_glossary_id():
    """Get a unique ID. Attempts to delete glossary with this ID after test."""
    glossary_id = 'must-start-with-letters-' + str(uuid.uuid1())

    yield glossary_id

    try:
        translate_delete_glossary.sample_delete_glossary(PROJECT_ID, glossary_id)
    except Exception:
        pass

def test_create_glossary(capsys, unique_glossary_id):
    translate_create_glossary.sample_create_glossary(PROJECT_ID, 'en', 'es', GLOSSARY_INPUT_URI, unique_glossary_id)
    out, _ = capsys.readouterr()
    assert 'Created' in out
    assert unique_glossary_id in out
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out

def test_delete_glossary(capsys, unique_glossary_id):
    translate_create_glossary.sample_create_glossary(PROJECT_ID, 'en', 'es', GLOSSARY_INPUT_URI, unique_glossary_id)
    translate_delete_glossary.sample_delete_glossary(PROJECT_ID, unique_glossary_id)
    out, _ = capsys.readouterr()
    assert 'us-central1' in out
    assert unique_glossary_id in out