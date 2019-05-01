# Copyright 2017 Google, Inc.
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
import tempfile

from google.cloud import storage
import pytest

import requester_pays

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
PROJECT = os.environ['GCLOUD_PROJECT']


def test_enable_requester_pays(capsys):
    requester_pays.enable_requester_pays(BUCKET)
    out, _ = capsys.readouterr()
    assert 'Requester Pays has been enabled for {}'.format(BUCKET) in out


def test_disable_requester_pays(capsys):
    requester_pays.disable_requester_pays(BUCKET)
    out, _ = capsys.readouterr()
    assert 'Requester Pays has been disabled for {}'.format(BUCKET) in out


def test_get_requester_pays_status(capsys):
    requester_pays.get_requester_pays_status(BUCKET)
    out, _ = capsys.readouterr()
    assert 'Requester Pays is disabled for {}'.format(BUCKET) in out


@pytest.fixture
def test_blob():
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage.Client().bucket(BUCKET)
    blob = bucket.blob('storage_snippets_test_sigil')
    blob.upload_from_string('Hello, is it me you\'re looking for?')
    return blob


def test_download_file_requester_pays(test_blob, capsys):
    with tempfile.NamedTemporaryFile() as dest_file:
        requester_pays.download_file_requester_pays(
            BUCKET,
            PROJECT,
            test_blob.name,
            dest_file.name)

        assert dest_file.read()
