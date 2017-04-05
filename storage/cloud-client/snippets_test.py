# Copyright 2016 Google, Inc.
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
import google.cloud.exceptions
import pytest
import requests

import snippets

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


@pytest.fixture
def test_blob():
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage.Client().bucket(BUCKET)
    blob = bucket.blob('storage_snippets_test_sigil')
    blob.upload_from_string('Hello, is it me you\'re looking for?')
    return blob


def test_list_blobs(test_blob, capsys):
    snippets.list_blobs(BUCKET)
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_list_blobs_with_prefix(test_blob, capsys):
    snippets.list_blobs_with_prefix(
        BUCKET,
        prefix='storage_snippets')
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_upload_blob():
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b'test')

        snippets.upload_blob(
            BUCKET,
            source_file.name,
            'test_upload_blob')


def test_download_blob(test_blob):
    with tempfile.NamedTemporaryFile() as dest_file:
        snippets.download_blob(
            BUCKET,
            test_blob.name,
            dest_file.name)

        assert dest_file.read()


def test_blob_metadata(test_blob, capsys):
    snippets.blob_metadata(BUCKET, test_blob.name)
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_delete_blob(test_blob):
    snippets.delete_blob(
        BUCKET,
        test_blob.name)


def test_make_blob_public(test_blob):
    snippets.make_blob_public(
        BUCKET,
        test_blob.name)

    r = requests.get(test_blob.public_url)
    assert r.text == 'Hello, is it me you\'re looking for?'


def test_generate_signed_url(test_blob, capsys):
    snippets.generate_signed_url(
        BUCKET,
        test_blob.name)

    out, _ = capsys.readouterr()
    url = out.rsplit().pop()

    r = requests.get(url)
    assert r.text == 'Hello, is it me you\'re looking for?'


def test_rename_blob(test_blob):
    bucket = storage.Client().bucket(BUCKET)

    try:
        bucket.delete_blob('test_rename_blob')
    except google.cloud.exceptions.exceptions.NotFound:
        pass

    snippets.rename_blob(bucket.name, test_blob.name, 'test_rename_blob')

    assert bucket.get_blob('test_rename_blob') is not None
    assert bucket.get_blob(test_blob.name) is None


def test_copy_blob(test_blob):
    bucket = storage.Client().bucket(BUCKET)

    try:
        bucket.delete_blob('test_copy_blob')
    except google.cloud.exceptions.NotFound:
        pass

    snippets.copy_blob(
        bucket.name, test_blob.name, bucket.name, 'test_copy_blob')

    assert bucket.get_blob('test_copy_blob') is not None
    assert bucket.get_blob(test_blob.name) is not None
