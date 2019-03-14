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
import beta_snippets
from google.cloud import storage

PROJECT_ID = os.environ['GCLOUD_PROJECT']


def test_translate_text(capsys):
    beta_snippets.translate_text(PROJECT_ID, 'Hello world')
    out, _ = capsys.readouterr()
    assert 'Zdravo svet' in out


def test_batch_translate_text(capsys):
    beta_snippets.batch_translate_text(
        PROJECT_ID,
        'gs://cloud-samples-data/translation/text.txt',
        'gs://{}/translation/BATCH_TRANSLATION_OUTPUT/'.format(PROJECT_ID))
    out, _ = capsys.readouterr()
    assert 'Total Characters: 13' in out
    assert 'Translated Characters: 13' in out

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(PROJECT_ID)

    blobs = bucket.list_blobs(prefix='translation/BATCH_TRANSLATION_OUTPUT')

    for blob in blobs:
        blob.delete()


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


def test_create_glossary(capsys):
    beta_snippets.create_glossary(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out


def test_get_glossary(capsys):
    beta_snippets.get_glossary(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out


def test_list_glossary(capsys):
    beta_snippets.list_glossaries(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'gs://cloud-samples-data/translation/glossary.csv' in out


def test_translate_text_with_glossary(capsys):
    beta_snippets.translate_text_with_glossary(PROJECT_ID, 'directions')
    out, _ = capsys.readouterr()
    assert 'direcciones' in out


def test_delete_glossary(capsys):
    beta_snippets.delete_glossary(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert PROJECT_ID in out
    assert 'us-central1' in out
    assert 'glossary' in out
