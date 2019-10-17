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
import uuid
import translate_v3_create_glossary
import translate_v3_delete_glossary
import translate_v3_translate_text_with_glossary_and_model
import pytest

PROJECT_ID = os.environ['GCLOUD_PROJECT']
MODEL_ID = os.environ['AUTOML_TRANSLATION_MODEL_ID']

#setup and teardown
@pytest.fixture(scope='session')
def glossary():
    """Get the ID of a glossary available to session (do not mutate/delete)."""
    glossary_id = 'must-start-with-letters-' + str(uuid.uuid1())
    translate_v3_create_glossary.sample_create_glossary(PROJECT_ID, 'gs://translation_samples_beta/glossaries/glossary.csv', glossary_id)

    yield glossary_id

    try:
        translate_v3_delete_glossary.sample_delete_glossary(PROJECT_ID, glossary_id)
    except Exception:
        pass

def test_translate_text_with_glossary_and_model(capsys, glossary):
    translate_v3_translate_text_with_glossary_and_model.sample_translate_text_glossary_and_model(
        MODEL_ID,
        glossary,
        "That' il do it. deception",
        "ja",
        "en",
        PROJECT_ID,
        "us-central1")
    out, _ = capsys.readouterr()
    assert 'それはそうだ' in out # custom model
    assert '欺く' in out # glossary
