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

import storage_add_bucket_label
import storage_bucket_delete_default_kms_key
import storage_change_default_storage_class
import storage_change_file_storage_class
import storage_compose_file
import storage_configure_retries
import storage_copy_file
import storage_copy_file_archived_generation
import storage_cors_configuration
import storage_create_bucket_class_location
import storage_define_bucket_website_configuration
import storage_delete_file
import storage_delete_file_archived_generation
import storage_disable_bucket_lifecycle_management
import storage_disable_versioning
import storage_download_file
import storage_download_public_file
import storage_enable_bucket_lifecycle_management
import storage_enable_versioning
import storage_generate_signed_post_policy_v4
import storage_generate_signed_url_v2
import storage_generate_signed_url_v4
import storage_generate_upload_signed_url_v4
import storage_get_bucket_labels
import storage_get_bucket_metadata
import storage_get_metadata
import storage_get_service_account
import storage_list_buckets
import storage_list_file_archived_generations
import storage_list_files
import storage_list_files_with_prefix
import storage_make_public
import storage_move_file
import storage_object_get_kms_key
import storage_remove_bucket_label
import storage_remove_cors_configuration
import storage_rename_file
import storage_set_bucket_default_kms_key
import storage_set_metadata
import storage_upload_file
import storage_upload_with_kms_key

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


@pytest.fixture(scope="function")
def test_public_bucket():
    # The new projects don't allow to make a bucket available to public, so
    # for some tests we need to use the old main project for now.
    original_value = os.environ['GOOGLE_CLOUD_PROJECT']
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['MAIN_GOOGLE_CLOUD_PROJECT']
    bucket = None
    while bucket is None or bucket.exists():
        storage_client = storage.Client()
        bucket_name = "storage-snippets-test-{}".format(uuid.uuid4())
        bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    yield bucket
    bucket.delete(force=True)
    # Set the value back.
    os.environ['GOOGLE_CLOUD_PROJECT'] = original_value


@pytest.fixture
def test_blob(test_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_bucket
    blob = bucket.blob("storage_snippets_test_sigil-{}".format(uuid.uuid4()))
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


@pytest.fixture(scope="function")
def test_public_blob(test_public_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_public_bucket
    blob = bucket.blob("storage_snippets_test_sigil-{}".format(uuid.uuid4()))
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


@pytest.fixture
def test_bucket_create():
    """Yields a bucket object that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "storage-snippets-test-{}".format(uuid.uuid4())
        bucket = storage.Client().bucket(bucket_name)
    yield bucket
    bucket.delete(force=True)


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


def test_make_blob_public(test_public_blob):
    storage_make_public.make_blob_public(
        test_public_blob.bucket.name, test_public_blob.name)

    r = requests.get(test_public_blob.public_url)
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
        url, data=content, headers={"content-type": "application/octet-stream"},
    )

    bucket = storage.Client().bucket(test_bucket.name)
    blob = bucket.blob(blob_name)
    assert blob.download_as_string() == content


def test_generate_signed_policy_v4(test_bucket, capsys):
    blob_name = "storage_snippets_test_form"
    short_name = storage_generate_signed_post_policy_v4
    form = short_name.generate_signed_post_policy_v4(test_bucket.name, blob_name)
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
        print("test_rename_blob not found in bucket {}".format(bucket.name))

    storage_rename_file.rename_blob(bucket.name, test_blob.name, "test_rename_blob")

    assert bucket.get_blob("test_rename_blob") is not None
    assert bucket.get_blob(test_blob.name) is None


def test_move_blob(test_bucket_create, test_blob):
    bucket = test_blob.bucket
    storage.Client().create_bucket(test_bucket_create)

    try:
        test_bucket_create.delete_blob("test_move_blob")
    except google.cloud.exceptions.NotFound:
        print("test_move_blob not found in bucket {}".format(test_bucket_create.name))

    storage_move_file.move_blob(
        bucket.name, test_blob.name, test_bucket_create.name, "test_move_blob"
    )

    assert test_bucket_create.get_blob("test_move_blob") is not None
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
    bucket = storage_enable_bucket_lifecycle_management.enable_bucket_lifecycle_management(
        test_bucket
    )
    out, _ = capsys.readouterr()
    assert "[]" in out
    assert "Lifecycle management is enable" in out
    assert len(list(bucket.lifecycle_rules)) > 0

    bucket = storage_disable_bucket_lifecycle_management.disable_bucket_lifecycle_management(
        test_bucket
    )
    out, _ = capsys.readouterr()
    assert "[]" in out
    assert len(list(bucket.lifecycle_rules)) == 0


def test_create_bucket_class_location(test_bucket_create):
    bucket = storage_create_bucket_class_location.create_bucket_class_location(
        test_bucket_create.name
    )

    assert bucket.location == "US"
    assert bucket.storage_class == "COLDLINE"


def test_bucket_delete_default_kms_key(test_bucket, capsys):
    test_bucket.default_kms_key_name = KMS_KEY
    test_bucket.patch()

    assert test_bucket.default_kms_key_name == KMS_KEY

    bucket = storage_bucket_delete_default_kms_key.bucket_delete_default_kms_key(
        test_bucket.name
    )

    out, _ = capsys.readouterr()
    assert bucket.default_kms_key_name is None
    assert bucket.name in out


def test_get_service_account(capsys):
    storage_get_service_account.get_service_account()

    out, _ = capsys.readouterr()

    assert "@gs-project-accounts.iam.gserviceaccount.com" in out


def test_download_public_file(test_public_blob):
    storage_make_public.make_blob_public(
        test_public_blob.bucket.name, test_public_blob.name)
    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_public_file.download_public_file(
            test_public_blob.bucket.name, test_public_blob.name, dest_file.name
        )

        assert dest_file.read() == b"Hello, is it me you're looking for?"


def test_define_bucket_website_configuration(test_bucket):
    bucket = storage_define_bucket_website_configuration.define_bucket_website_configuration(
        test_bucket.name, "index.html", "404.html"
    )

    website_val = {"mainPageSuffix": "index.html", "notFoundPage": "404.html"}

    assert bucket._properties["website"] == website_val


def test_object_get_kms_key(test_bucket):
    with tempfile.NamedTemporaryFile() as source_file:
        storage_upload_with_kms_key.upload_blob_with_kms(
            test_bucket.name, source_file.name, "test_upload_blob_encrypted", KMS_KEY
        )
    kms_key = storage_object_get_kms_key.object_get_kms_key(
        test_bucket.name, "test_upload_blob_encrypted"
    )

    assert kms_key.startswith(KMS_KEY)


def test_storage_compose_file(test_bucket):
    source_files = ["test_upload_blob_1", "test_upload_blob_2"]
    for source in source_files:
        blob = test_bucket.blob(source)
        blob.upload_from_string(source)

    with tempfile.NamedTemporaryFile() as dest_file:
        destination = storage_compose_file.compose_file(
            test_bucket.name, source_files[0], source_files[1], dest_file.name
        )
        composed = destination.download_as_string()

        assert composed.decode("utf-8") == source_files[0] + source_files[1]


def test_cors_configuration(test_bucket, capsys):
    bucket = storage_cors_configuration.cors_configuration(test_bucket)
    out, _ = capsys.readouterr()
    assert "Set CORS policies for bucket" in out
    assert len(bucket.cors) > 0

    bucket = storage_remove_cors_configuration.remove_cors_configuration(test_bucket)
    out, _ = capsys.readouterr()
    assert "Remove CORS policies for bucket" in out
    assert len(bucket.cors) == 0


def test_delete_blobs_archived_generation(test_blob, capsys):
    storage_delete_file_archived_generation.delete_file_archived_generation(
        test_blob.bucket.name, test_blob.name, test_blob.generation
    )
    out, _ = capsys.readouterr()
    assert "blob " + test_blob.name + " was deleted" in out
    blob = test_blob.bucket.get_blob(test_blob.name, generation=test_blob.generation)
    assert blob is None


def test_change_default_storage_class(test_bucket, capsys):
    bucket = storage_change_default_storage_class.change_default_storage_class(
        test_bucket
    )
    out, _ = capsys.readouterr()
    assert "Default storage class for bucket" in out
    assert bucket.storage_class == 'COLDLINE'


def test_change_file_storage_class(test_blob, capsys):
    blob = storage_change_file_storage_class.change_file_storage_class(
        test_blob.bucket.name, test_blob.name
    )
    out, _ = capsys.readouterr()
    assert "Blob {} in bucket {}". format(blob.name, blob.bucket.name) in out
    assert blob.storage_class == 'NEARLINE'


def test_copy_file_archived_generation(test_blob):
    bucket = storage.Client().bucket(test_blob.bucket.name)

    try:
        bucket.delete_blob("test_copy_blob")
    except google.cloud.exceptions.NotFound:
        pass

    storage_copy_file_archived_generation.copy_file_archived_generation(
        bucket.name, test_blob.name, bucket.name, "test_copy_blob", test_blob.generation
    )

    assert bucket.get_blob("test_copy_blob") is not None
    assert bucket.get_blob(test_blob.name) is not None


def test_list_blobs_archived_generation(test_blob, capsys):
    storage_list_file_archived_generations.list_file_archived_generations(
        test_blob.bucket.name
    )
    out, _ = capsys.readouterr()
    assert str(test_blob.generation) in out


def test_storage_configure_retries(test_blob, capsys):
    storage_configure_retries.configure_retries(test_blob.bucket.name, test_blob.name)

    # This simply checks if the retry configurations were set and printed as intended.
    out, _ = capsys.readouterr()
    assert "The following library method is customized to be retried" in out
    assert "_should_retry" in out
    assert "initial=1.5, maximum=45.0, multiplier=1.2, deadline=500.0" in out
