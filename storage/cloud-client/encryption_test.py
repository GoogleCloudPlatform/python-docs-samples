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

import base64
import os
import tempfile
import uuid

from google.api_core.exceptions import NotFound
from google.cloud import storage
from google.cloud.storage import Blob
import pytest

import storage_download_encrypted_file
import storage_generate_encryption_key
import storage_object_csek_to_cmek
import storage_rotate_encryption_key
import storage_upload_encrypted_file

BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
KMS_KEY = os.environ["CLOUD_KMS_KEY"]

TEST_ENCRYPTION_KEY = "brtJUWneL92g5q0N2gyDSnlPSYAiIVZ/cWgjyZNeMy0="
TEST_ENCRYPTION_KEY_DECODED = base64.b64decode(TEST_ENCRYPTION_KEY)

TEST_ENCRYPTION_KEY_2 = "o4OD7SWCaPjfeEGhAY+YCgMdY9UW+OJ8mvfWD9lNtO4="
TEST_ENCRYPTION_KEY_2_DECODED = base64.b64decode(TEST_ENCRYPTION_KEY_2)


def test_generate_encryption_key(capsys):
    storage_generate_encryption_key.generate_encryption_key()
    out, _ = capsys.readouterr()
    encoded_key = out.split(":", 1).pop().strip()
    key = base64.b64decode(encoded_key)
    assert len(key) == 32, "Returned key should be 32 bytes"


def test_upload_encrypted_blob():
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b"test")

        storage_upload_encrypted_file.upload_encrypted_blob(
            BUCKET,
            source_file.name,
            "test_encrypted_upload_blob",
            TEST_ENCRYPTION_KEY,
        )


@pytest.fixture(scope="module")
def test_blob():
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage.Client().bucket(BUCKET)
    blob_name = "test_blob_{}".format(uuid.uuid4().hex)
    blob = Blob(
        blob_name,
        bucket,
        encryption_key=TEST_ENCRYPTION_KEY_DECODED,
    )
    content = "Hello, is it me you're looking for?"
    blob.upload_from_string(content)

    yield blob.name, content

    # To delete an encrypted blob, you have to provide the same key
    # used for the blob. When you provide a wrong key, you'll get
    # NotFound.
    try:
        # Clean up for the case that the rotation didn't occur.
        blob.delete()
    except NotFound as e:
        # For the case that the rotation succeeded.
        print("Ignoring 404, detail: {}".format(e))
        blob = Blob(
            blob_name,
            bucket,
            encryption_key=TEST_ENCRYPTION_KEY_2_DECODED
        )
        blob.delete()


def test_download_blob(test_blob):
    test_blob_name, test_blob_content = test_blob
    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_encrypted_file.download_encrypted_blob(
            BUCKET, test_blob_name, dest_file.name, TEST_ENCRYPTION_KEY
        )

        downloaded_content = dest_file.read().decode("utf-8")
        assert downloaded_content == test_blob_content


def test_rotate_encryption_key(test_blob):
    test_blob_name, test_blob_content = test_blob
    storage_rotate_encryption_key.rotate_encryption_key(
        BUCKET, test_blob_name, TEST_ENCRYPTION_KEY, TEST_ENCRYPTION_KEY_2
    )

    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_encrypted_file.download_encrypted_blob(
            BUCKET, test_blob_name, dest_file.name, TEST_ENCRYPTION_KEY_2
        )

        downloaded_content = dest_file.read().decode("utf-8")
        assert downloaded_content == test_blob_content


def test_object_csek_to_cmek(test_blob):
    test_blob_name, test_blob_content = test_blob
    cmek_blob = storage_object_csek_to_cmek.object_csek_to_cmek(
        BUCKET, test_blob_name, TEST_ENCRYPTION_KEY_2, KMS_KEY
    )

    assert cmek_blob.download_as_string(), test_blob_content
