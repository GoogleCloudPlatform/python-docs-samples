# Copyright 2016, Google, Inc.
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

import tempfile

from gcloud import storage
import manage_blobs
import pytest


@pytest.fixture
def test_blob(cloud_config):
    bucket = storage.Client().bucket(cloud_config.storage_bucket)
    blob = bucket.blob('manage_blobs_test_sigil')
    blob.upload_from_string('Hello, is it me you\'re looking for?')
    return blob.name


def test_list_blobs(test_blob, cloud_config, capsys):
    manage_blobs.list_blobs(cloud_config.storage_bucket)
    out, _ = capsys.readouterr()
    assert test_blob in out


def test_upload_blob(cloud_config):
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b'test')

        manage_blobs.upload_blob(
            cloud_config.storage_bucket,
            source_file.name, 'test_upload_blob')


def test_download_blob(test_blob, cloud_config):
    with tempfile.NamedTemporaryFile() as dest_file:
        manage_blobs.download_blob(
            cloud_config.storage_bucket,
            test_blob,
            dest_file.name)

        assert dest_file.read()


def test_delete_blob(test_blob, cloud_config):
    manage_blobs.delete_blob(
        cloud_config.storage_bucket,
        test_blob)
