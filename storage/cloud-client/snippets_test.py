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
import time
import uuid

from google.cloud import storage
import google.cloud.exceptions
import pytest
import requests

import storage_copy_file
import storage_add_bucket_label
import storage_delete_file
import storage_download_file
import storage_get_bucket_labels
import storage_get_bucket_metadata
import storage_get_metadata
import storage_set_metadata
import storage_list_buckets
import storage_list_files_with_prefix
import storage_list_files
import storage_make_public
import storage_remove_bucket_label
import storage_move_file
import storage_upload_file
import storage_upload_with_kms_key
import storage_generate_signed_url_v2
import storage_generate_signed_url_v4
import storage_generate_upload_signed_url_v4
import storage_generate_signed_post_policy_v4
import storage_set_bucket_default_kms_key
import storage_enable_versioning
import storage_disable_versioning
import storage_enable_bucket_lifecycle_management
import storage_disable_bucket_lifecycle_management

KMS_KEY = os.environ["CLOUD_KMS_KEY"]


def test_enable_default_kms_key(test_bucket):
    storage_set_bucket_default_kms_key.enable_default_kms_key(
        bucket_name=test_bucket.name, kms_key_name=KMS_KEY
    )
    time.sleep(2)  # Let change propagate as needed
    bucket = storage.Client().get_bucket(test_bucket.name)
    assert bucket.default_kms_key_name.startswith(KMS_KEY)
    bucket.default_kms_key_name = None
    bucket.patch()


def test_get_bucket_labels(test_bucket):
    storage_get_bucket_labels.get_bucket_labels(test_bucket.name)


def test_add_bucket_label(test_bucket, capsys):
    storage_add_bucket_label.add_bucket_label(test_bucket.name)
    out, _ = capsys.readouterr()
    assert "example" in out


def test_remove_bucket_label(test_bucket, capsys):
    storage_add_bucket_label.add_bucket_label(test_bucket.name)
    storage_remove_bucket_label.remove_bucket_label(test_bucket.name)
    out, _ = capsys.readouterr()
    assert "Removed labels" in out


@pytest.fixture(scope="module")
def test_bucket():
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "storage-snippets-test-{}".format(uuid.uuid4())
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    bucket.delete(force=True)


@pytest.fixture
def test_blob(test_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_bucket
    blob = bucket.blob("storage_snippets_test_sigil-{}".format(uuid.uuid4()))
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


def test_list_buckets(test_bucket, capsys):
    storage_list_buckets.list_buckets()
    out, _ = capsys.readouterr()
    assert test_bucket.name in out


def test_list_blobs(test_blob, capsys):
    storage_list_files.list_blobs(test_blob.bucket.name)
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_bucket_metadata(test_bucket, capsys):
    storage_get_bucket_metadata.bucket_metadata(test_bucket.name)
    out, _ = capsys.readouterr()
    assert test_bucket.name in out


def test_list_blobs_with_prefix(test_blob, capsys):
    storage_list_files_with_prefix.list_blobs_with_prefix(
        test_blob.bucket.name, prefix="storage_snippets"
    )
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_upload_blob(test_bucket):
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b"test")

        storage_upload_file.upload_blob(
            test_bucket.name, source_file.name, "test_upload_blob"
        )


def test_upload_blob_with_kms(test_bucket):
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b"test")
        storage_upload_with_kms_key.upload_blob_with_kms(
            test_bucket.name, source_file.name, "test_upload_blob_encrypted", KMS_KEY
        )
        bucket = storage.Client().bucket(test_bucket.name)
        kms_blob = bucket.get_blob("test_upload_blob_encrypted")
        assert kms_blob.kms_key_name.startswith(KMS_KEY)


def test_download_blob(test_blob):
    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_file.download_blob(
            test_blob.bucket.name, test_blob.name, dest_file.name
        )

        assert dest_file.read()


def test_blob_metadata(test_blob, capsys):
    storage_get_metadata.blob_metadata(test_blob.bucket.name, test_blob.name)
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_set_blob_metadata(test_blob, capsys):
    storage_set_metadata.set_blob_metadata(test_blob.bucket.name, test_blob.name)
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_delete_blob(test_blob):
    storage_delete_file.delete_blob(test_blob.bucket.name, test_blob.name)


def test_make_blob_public(test_blob):
    storage_make_public.make_blob_public(test_blob.bucket.name, test_blob.name)

    r = requests.get(test_blob.public_url)
    assert r.text == "Hello, is it me you're looking for?"


def test_generate_signed_url(test_blob, capsys):
    url = storage_generate_signed_url_v2.generate_signed_url(
        test_blob.bucket.name, test_blob.name
    )

    r = requests.get(url)
    assert r.text == "Hello, is it me you're looking for?"


def test_generate_download_signed_url_v4(test_blob, capsys):
    url = storage_generate_signed_url_v4.generate_download_signed_url_v4(
        test_blob.bucket.name, test_blob.name
    )

    r = requests.get(url)
    assert r.text == "Hello, is it me you're looking for?"


def test_generate_upload_signed_url_v4(test_bucket, capsys):
    blob_name = "storage_snippets_test_upload"
    content = b"Uploaded via v4 signed url"
    url = storage_generate_upload_signed_url_v4.generate_upload_signed_url_v4(
        test_bucket.name, blob_name
    )

    requests.put(
        url,
        data=content,
        headers={"content-type": "application/octet-stream"},
    )

    bucket = storage.Client().bucket(test_bucket.name)
    blob = bucket.blob(blob_name)
    assert blob.download_as_string() == content


def test_generate_signed_policy_v4(test_bucket, capsys):
    blob_name = "storage_snippets_test_form"
    short_name = storage_generate_signed_post_policy_v4
    form = short_name.generate_signed_post_policy_v4(
        test_bucket.name, blob_name
    )
    assert "name='key' value='{}'".format(blob_name) in form
    assert "name='x-goog-signature'" in form
    assert "name='x-goog-date'" in form
    assert "name='x-goog-credential'" in form
    assert "name='x-goog-algorithm' value='GOOG4-RSA-SHA256'" in form
    assert "name='policy'" in form
    assert "name='x-goog-meta-test' value='data'" in form
    assert "type='file' name='file'/>" in form


def test_rename_blob(test_blob):
    bucket = storage.Client().bucket(test_blob.bucket.name)

    try:
        bucket.delete_blob("test_rename_blob")
    except google.cloud.exceptions.exceptions.NotFound:
        pass

    storage_move_file.rename_blob(
        bucket.name, test_blob.name, "test_rename_blob"
    )

    assert bucket.get_blob("test_rename_blob") is not None
    assert bucket.get_blob(test_blob.name) is None


def test_copy_blob(test_blob):
    bucket = storage.Client().bucket(test_blob.bucket.name)

    try:
        bucket.delete_blob("test_copy_blob")
    except google.cloud.exceptions.NotFound:
        pass

    storage_copy_file.copy_blob(
        bucket.name, test_blob.name, bucket.name, "test_copy_blob"
    )

    assert bucket.get_blob("test_copy_blob") is not None
    assert bucket.get_blob(test_blob.name) is not None


def test_versioning(test_bucket, capsys):
    bucket = storage_enable_versioning.enable_versioning(test_bucket)
    out, _ = capsys.readouterr()
    assert "Versioning was enabled for bucket" in out
    assert bucket.versioning_enabled is True

    bucket = storage_disable_versioning.disable_versioning(test_bucket)
    out, _ = capsys.readouterr()
    assert "Versioning was disabled for bucket" in out
    assert bucket.versioning_enabled is False


def test_bucket_lifecycle_management(test_bucket, capsys):
    bucket = storage_enable_bucket_lifecycle_management.\
        enable_bucket_lifecycle_management(test_bucket)
    out, _ = capsys.readouterr()
    assert "[]" in out
    assert "Lifecycle management is enable" in out
    assert len(list(bucket.lifecycle_rules)) > 0

    bucket = storage_disable_bucket_lifecycle_management.\
        disable_bucket_lifecycle_management(test_bucket)
    out, _ = capsys.readouterr()
    assert "[]" in out
    assert len(list(bucket.lifecycle_rules)) == 0
