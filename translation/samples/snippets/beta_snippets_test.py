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
import uuid
import beta_snippets
from google.cloud import storage

PROJECT_ID = os.environ['GCLOUD_PROJECT']


@pytest.fixture(scope='function')
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = str(uuid.uuid1())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


@pytest.fixture(scope='session')
def glossary():
    """Get the ID of a glossary available to session (do not mutate/delete)."""
    glossary_id = 'must-start-with-letters-' + str(uuid.uuid1())
    beta_snippets.create_glossary(PROJECT_ID, glossary_id)

    yield glossary_id

    try:
        beta_snippets.delete_glossary(PROJECT_ID, glossary_id)
    except Exception:
        pass


@pytest.fixture(scope='function')
def unique_glossary_id():
    """Get a unique ID. Attempts to delete glossary with this ID after test."""
    glossary_id = 'must-start-with-letters-' + str(uuid.uuid1())

    yield glossary_id

    try:
        beta_snippets.delete_glossary(PROJECT_ID, glossary_id)
    except Exception:
        pass


def test_translate_text(capsys):
    beta_snippets.translate_text(PROJECT_ID, 'Hello world')
    out, _ = capsys.readouterr()
    assert 'Zdravo svet' in out or 'Pozdrav svijetu' in out


def test_batch_translate_text(capsys, bucket):
    beta_snippets.batch_translate_text(
        PROJECT_ID,
        'gs://cloud-samples-data/translation/text.txt',
        'gs://{}/translation/BATCH_TRANSLATION_OUTPUT/'.format(bucket.name))
    out, _ = capsys.readouterr()
    assert 'Total Characters: 13' in out
    assert 'Translated Characters: 13' in out


def test_detect_language(capsys):
    beta_snippets.detect_language(PROJECT_ID, 'Hæ sæta')
    out, _ = capsys.readouterr()
    assert 'is' in out


def test_list_languages(capsys):
    beta_snippets.list_languages(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'zh-CN' in out


def test_list_languages_with_target(capsys):
    beta_snippets.list_languages_with_target(PROJECT_ID, 'is')
    out, _ = capsys.readouterr()
    assert u'Language Code: sq' in out
    assert u'Display Name: albanska' in out


def test_create_glossary(capsys, unique_glossary_id):
    beta_snippets.create_glossary(PROJECT_ID, unique_glossary_id)
    out, _ = capsys.readouterr()
    assert 'Created' in out
    assert unique_glossary_id in out
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out


def test_get_glossary(capsys, glossary):
    beta_snippets.get_glossary(PROJECT_ID, glossary)
    out, _ = capsys.readouterr()
    assert glossary in out
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out


def test_list_glossary(capsys, glossary):
    beta_snippets.list_glossaries(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert glossary in out
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out


def test_translate_text_with_glossary(capsys, glossary):
    beta_snippets.translate_text_with_glossary(
            PROJECT_ID, glossary, 'account')
    out, _ = capsys.readouterr()
    assert 'cuenta' in out


def test_delete_glossary(capsys, unique_glossary_id):
    beta_snippets.create_glossary(PROJECT_ID, unique_glossary_id)
    beta_snippets.delete_glossary(PROJECT_ID, unique_glossary_id)
    out, _ = capsys.readouterr()
    assert 'us-central1' in out
    assert unique_glossary_id in out
