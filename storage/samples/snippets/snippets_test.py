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

import asyncio
import io
import os
import tempfile
import time
import uuid

from google.cloud import storage
import google.cloud.exceptions
import pytest
import requests

import storage_add_bucket_label
import storage_async_download
import storage_async_upload
import storage_batch_request
import storage_bucket_delete_default_kms_key
import storage_change_default_storage_class
import storage_change_file_storage_class
import storage_compose_file
import storage_configure_retries
import storage_copy_file
import storage_copy_file_archived_generation
import storage_cors_configuration
import storage_create_bucket_class_location
import storage_create_bucket_dual_region
import storage_create_bucket_hierarchical_namespace
import storage_create_bucket_object_retention
import storage_define_bucket_website_configuration
import storage_delete_file
import storage_delete_file_archived_generation
import storage_disable_bucket_lifecycle_management
import storage_disable_soft_delete
import storage_disable_versioning
import storage_download_byte_range
import storage_download_file
import storage_download_into_memory
import storage_download_public_file
import storage_download_to_stream
import storage_enable_bucket_lifecycle_management
import storage_enable_versioning
import storage_generate_signed_post_policy_v4
import storage_generate_signed_url_v2
import storage_generate_signed_url_v4
import storage_generate_upload_signed_url_v4
import storage_get_autoclass
import storage_get_bucket_labels
import storage_get_bucket_metadata
import storage_get_metadata
import storage_get_service_account
import storage_get_soft_delete_policy
import storage_get_soft_deleted_bucket
import storage_list_buckets
import storage_list_file_archived_generations
import storage_list_files
import storage_list_files_with_prefix
import storage_list_soft_deleted_buckets
import storage_list_soft_deleted_object_versions
import storage_list_soft_deleted_objects
import storage_make_public
import storage_move_file
import storage_move_file_atomically
import storage_object_get_kms_key
import storage_remove_bucket_label
import storage_remove_cors_configuration
import storage_rename_file
import storage_restore_object
import storage_restore_soft_deleted_bucket
import storage_set_autoclass
import storage_set_bucket_default_kms_key
import storage_set_client_endpoint
import storage_set_metadata
import storage_set_object_retention_policy
import storage_set_soft_delete_policy
import storage_trace_quickstart
import storage_transfer_manager_download_bucket
import storage_transfer_manager_download_chunks_concurrently
import storage_transfer_manager_download_many
import storage_transfer_manager_upload_chunks_concurrently
import storage_transfer_manager_upload_directory
import storage_transfer_manager_upload_many
import storage_upload_file
import storage_upload_from_memory
import storage_upload_from_stream
import storage_upload_with_kms_key

KMS_KEY = os.environ.get("CLOUD_KMS_KEY")


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
        bucket_name = f"storage-snippets-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    bucket.delete(force=True)


@pytest.fixture(scope="module")
def test_soft_deleted_bucket():
    """Yields a soft-deleted bucket."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"storage-snippets-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    # [Assumption] Bucket is created with default policy , ie soft delete on.
    bucket.delete()
    yield bucket


@pytest.fixture(scope="function")
def test_soft_delete_enabled_bucket():
    """Yields a bucket with soft-delete enabled that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"storage-snippets-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    # Soft-delete retention for 7 days (minimum allowed by API)
    bucket.soft_delete_policy.retention_duration_seconds = 7 * 24 * 60 * 60
    # Soft-delete requires a region
    bucket.create(location="US-CENTRAL1")
    yield bucket
    bucket.delete(force=True)


@pytest.fixture(scope="function")
def test_public_bucket():
    # The new projects don't allow to make a bucket available to public, so
    # for some tests we need to use the old main project for now.
    original_value = os.environ["GOOGLE_CLOUD_PROJECT"]
    os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["MAIN_GOOGLE_CLOUD_PROJECT"]
    bucket = None
    while bucket is None or bucket.exists():
        storage_client = storage.Client()
        bucket_name = f"storage-snippets-test-{uuid.uuid4()}"
        bucket = storage_client.bucket(bucket_name)
    storage_client.create_bucket(bucket)
    yield bucket
    bucket.delete(force=True)
    # Set the value back.
    os.environ["GOOGLE_CLOUD_PROJECT"] = original_value


@pytest.fixture(scope="module")
def new_bucket_obj():
    """Yields a new bucket object that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"storage-snippets-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    yield bucket
    bucket.delete(force=True)


@pytest.fixture
def test_blob(test_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_bucket
    blob = bucket.blob(f"storage_snippets_test_sigil-{uuid.uuid4()}")
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


@pytest.fixture(scope="function")
def test_public_blob(test_public_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_public_bucket
    blob = bucket.blob(f"storage_snippets_test_sigil-{uuid.uuid4()}")
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


@pytest.fixture
def test_bucket_create():
    """Yields a bucket object that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"storage-snippets-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    yield bucket
    bucket.delete(force=True)


def test_list_buckets(test_bucket, capsys):
    storage_list_buckets.list_buckets()
    out, _ = capsys.readouterr()
    assert test_bucket.name in out


def test_list_soft_deleted_buckets(test_soft_deleted_bucket, capsys):
    storage_list_soft_deleted_buckets.list_soft_deleted_buckets()
    out, _ = capsys.readouterr()
    assert test_soft_deleted_bucket.name in out


def test_list_blobs(test_blob, capsys):
    storage_list_files.list_blobs(test_blob.bucket.name)
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_bucket_metadata(test_bucket, capsys):
    storage_get_bucket_metadata.bucket_metadata(test_bucket.name)
    out, _ = capsys.readouterr()
    assert test_bucket.name in out


def test_get_soft_deleted_bucket(test_soft_deleted_bucket, capsys):
    storage_get_soft_deleted_bucket.get_soft_deleted_bucket(
        test_soft_deleted_bucket.name, test_soft_deleted_bucket.generation
    )
    out, _ = capsys.readouterr()
    assert test_soft_deleted_bucket.name in out


def test_restore_soft_deleted_bucket(test_soft_deleted_bucket, capsys):
    storage_restore_soft_deleted_bucket.restore_bucket(
        test_soft_deleted_bucket.name, test_soft_deleted_bucket.generation
    )
    out, _ = capsys.readouterr()
    assert test_soft_deleted_bucket.name in out


def test_list_blobs_with_prefix(test_blob, capsys):
    storage_list_files_with_prefix.list_blobs_with_prefix(
        test_blob.bucket.name, prefix="storage_snippets"
    )
    out, _ = capsys.readouterr()
    assert test_blob.name in out


def test_upload_blob(test_bucket):
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b"test")
        source_file.flush()

        storage_upload_file.upload_blob(
            test_bucket.name, source_file.name, "test_upload_blob"
        )


def test_upload_blob_from_memory(test_bucket, capsys):
    storage_upload_from_memory.upload_blob_from_memory(
        test_bucket.name, "Hello, is it me you're looking for?", "test_upload_blob"
    )
    out, _ = capsys.readouterr()

    assert "Hello, is it me you're looking for?" in out


def test_upload_blob_from_stream(test_bucket, capsys):
    file_obj = io.BytesIO()
    file_obj.write(b"This is test data.")
    storage_upload_from_stream.upload_blob_from_stream(
        test_bucket.name, file_obj, "test_upload_blob"
    )
    out, _ = capsys.readouterr()

    assert "Stream data uploaded to test_upload_blob" in out


def test_upload_blob_with_kms(test_bucket):
    blob_name = f"test_upload_with_kms_{uuid.uuid4().hex}"
    with tempfile.NamedTemporaryFile() as source_file:
        source_file.write(b"test")
        source_file.flush()
        storage_upload_with_kms_key.upload_blob_with_kms(
            test_bucket.name,
            source_file.name,
            blob_name,
            KMS_KEY,
        )
        bucket = storage.Client().bucket(test_bucket.name)
        kms_blob = bucket.get_blob(blob_name)
        assert kms_blob.kms_key_name.startswith(KMS_KEY)
    test_bucket.delete_blob(blob_name)


def test_async_upload(bucket, capsys):
    asyncio.run(storage_async_upload.async_upload_blob(bucket.name))
    out, _ = capsys.readouterr()
    assert f"Uploaded 3 files to bucket {bucket.name}" in out


def test_async_download(test_bucket, capsys):
    object_count = 3
    source_files = [f"async_sample_blob_{x}" for x in range(object_count)]
    for source in source_files:
        blob = test_bucket.blob(source)
        blob.upload_from_string(source)

    asyncio.run(
        storage_async_download.async_download_blobs(test_bucket.name, *source_files)
    )
    out, _ = capsys.readouterr()
    for x in range(object_count):
        assert f"Downloaded storage object async_sample_blob_{x}" in out


def test_download_byte_range(test_blob):
    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_byte_range.download_byte_range(
            test_blob.bucket.name, test_blob.name, 0, 4, dest_file.name
        )
        assert dest_file.read() == b"Hello"


def test_download_blob(test_blob):
    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_file.download_blob(
            test_blob.bucket.name, test_blob.name, dest_file.name
        )

        assert dest_file.read()


def test_download_blob_into_memory(test_blob, capsys):
    storage_download_into_memory.download_blob_into_memory(
        test_blob.bucket.name, test_blob.name
    )
    out, _ = capsys.readouterr()

    assert "Hello, is it me you're looking for?" in out


def test_download_blob_to_stream(test_blob, capsys):
    file_obj = io.BytesIO()
    storage_download_to_stream.download_blob_to_stream(
        test_blob.bucket.name, test_blob.name, file_obj
    )
    out, _ = capsys.readouterr()

    file_obj.seek(0)
    content = file_obj.read()

    assert "Downloaded blob" in out
    assert b"Hello, is it me you're looking for?" in content


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


@pytest.mark.xfail(reason="wait until b/469643064 is fixed")
def test_make_blob_public(test_public_blob):
    storage_make_public.make_blob_public(
        test_public_blob.bucket.name, test_public_blob.name
    )

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
        url,
        data=content,
        headers={"content-type": "application/octet-stream"},
    )

    bucket = storage.Client().bucket(test_bucket.name)
    blob = bucket.blob(blob_name)
    assert blob.download_as_bytes() == content


def test_generate_signed_policy_v4(test_bucket, capsys):
    blob_name = "storage_snippets_test_form"
    short_name = storage_generate_signed_post_policy_v4
    form = short_name.generate_signed_post_policy_v4(test_bucket.name, blob_name)
    assert f"name='key' value='{blob_name}'" in form
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
        print(f"test_rename_blob not found in bucket {bucket.name}")

    storage_rename_file.rename_blob(bucket.name, test_blob.name, "test_rename_blob")

    assert bucket.get_blob("test_rename_blob") is not None
    assert bucket.get_blob(test_blob.name) is None


def test_move_blob(test_bucket_create, test_blob):
    bucket = test_blob.bucket
    storage.Client().create_bucket(test_bucket_create)

    try:
        test_bucket_create.delete_blob("test_move_blob")
    except google.cloud.exceptions.NotFound:
        print(f"test_move_blob not found in bucket {test_bucket_create.name}")

    storage_move_file.move_blob(
        bucket.name,
        test_blob.name,
        test_bucket_create.name,
        "test_move_blob",
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
        bucket.name,
        test_blob.name,
        bucket.name,
        "test_copy_blob",
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


def test_get_set_autoclass(new_bucket_obj, test_bucket, capsys):
    # Test default values when Autoclass is unset
    bucket = storage_get_autoclass.get_autoclass(test_bucket.name)
    out, _ = capsys.readouterr()
    assert "Autoclass enabled is set to False" in out
    assert bucket.autoclass_toggle_time is None
    assert bucket.autoclass_terminal_storage_class_update_time is None

    # Test enabling Autoclass at bucket creation
    new_bucket_obj.autoclass_enabled = True
    bucket = storage.Client().create_bucket(new_bucket_obj)
    assert bucket.autoclass_enabled is True
    assert bucket.autoclass_terminal_storage_class == "NEARLINE"

    # Test set terminal_storage_class to ARCHIVE
    bucket = storage_set_autoclass.set_autoclass(bucket.name)
    out, _ = capsys.readouterr()
    assert "Autoclass enabled is set to True" in out
    assert bucket.autoclass_enabled is True
    assert bucket.autoclass_terminal_storage_class == "ARCHIVE"

    # Test get Autoclass
    bucket = storage_get_autoclass.get_autoclass(bucket.name)
    out, _ = capsys.readouterr()
    assert "Autoclass enabled is set to True" in out
    assert bucket.autoclass_toggle_time is not None
    assert bucket.autoclass_terminal_storage_class_update_time is not None


def test_bucket_lifecycle_management(test_bucket, capsys):
    bucket = (
        storage_enable_bucket_lifecycle_management.enable_bucket_lifecycle_management(
            test_bucket
        )
    )
    out, _ = capsys.readouterr()
    assert "[]" in out
    assert "Lifecycle management is enable" in out
    assert len(list(bucket.lifecycle_rules)) > 0

    bucket = (
        storage_disable_bucket_lifecycle_management.disable_bucket_lifecycle_management(
            test_bucket
        )
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


def test_create_bucket_dual_region(test_bucket_create, capsys):
    location = "US"
    region_1 = "US-EAST1"
    region_2 = "US-WEST1"
    storage_create_bucket_dual_region.create_bucket_dual_region(
        test_bucket_create.name, location, region_1, region_2
    )
    out, _ = capsys.readouterr()
    assert f"Created bucket {test_bucket_create.name}" in out
    assert location in out
    assert region_1 in out
    assert region_2 in out
    assert "dual-region" in out


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


@pytest.mark.xfail(reason="wait until b/469643064 is fixed")
def test_download_public_file(test_public_blob):
    storage_make_public.make_blob_public(
        test_public_blob.bucket.name, test_public_blob.name
    )
    with tempfile.NamedTemporaryFile() as dest_file:
        storage_download_public_file.download_public_file(
            test_public_blob.bucket.name, test_public_blob.name, dest_file.name
        )

        assert dest_file.read() == b"Hello, is it me you're looking for?"


def test_define_bucket_website_configuration(test_bucket):
    bucket = (
        storage_define_bucket_website_configuration.define_bucket_website_configuration(
            test_bucket.name, "index.html", "404.html"
        )
    )

    website_val = {"mainPageSuffix": "index.html", "notFoundPage": "404.html"}

    assert bucket._properties["website"] == website_val


def test_object_get_kms_key(test_bucket):
    with tempfile.NamedTemporaryFile() as source_file:
        storage_upload_with_kms_key.upload_blob_with_kms(
            test_bucket.name,
            source_file.name,
            "test_upload_blob_encrypted",
            KMS_KEY,
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
            test_bucket.name,
            source_files[0],
            source_files[1],
            dest_file.name,
        )
        composed = destination.download_as_bytes()

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
    assert bucket.storage_class == "COLDLINE"


def test_change_file_storage_class(test_blob, capsys):
    blob = storage_change_file_storage_class.change_file_storage_class(
        test_blob.bucket.name,
        test_blob.name,
    )
    out, _ = capsys.readouterr()
    assert f"Blob {blob.name} in bucket {blob.bucket.name}" in out
    assert blob.storage_class == "NEARLINE"


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
    assert "initial=1.5, maximum=45.0, multiplier=1.2" in out
    assert "500" in out  # "deadline" or "timeout" depending on dependency ver.


def test_batch_request(test_bucket):
    blob1 = test_bucket.blob("b/1.txt")
    blob2 = test_bucket.blob("b/2.txt")
    blob1.upload_from_string("hello world")
    blob2.upload_from_string("hello world")

    storage_batch_request.batch_request(test_bucket.name, "b/")
    blob1.reload()
    blob2.reload()

    assert blob1.metadata.get("your-metadata-key") == "your-metadata-value"
    assert blob2.metadata.get("your-metadata-key") == "your-metadata-value"


def test_storage_set_client_endpoint(capsys):
    storage_set_client_endpoint.set_client_endpoint("https://storage.googleapis.com")
    out, _ = capsys.readouterr()

    assert "client initiated with endpoint: https://storage.googleapis.com" in out


def test_transfer_manager_snippets(test_bucket, capsys):
    BLOB_NAMES = [
        "test.txt",
        "test2.txt",
        "blobs/test.txt",
        "blobs/nesteddir/test.txt",
    ]

    with tempfile.TemporaryDirectory() as uploads:
        # Create dirs and nested dirs
        for name in BLOB_NAMES:
            relpath = os.path.dirname(name)
            os.makedirs(os.path.join(uploads, relpath), exist_ok=True)

        # Create files with nested dirs to exercise directory handling.
        for name in BLOB_NAMES:
            with open(os.path.join(uploads, name), "w") as f:
                f.write(name)

        storage_transfer_manager_upload_many.upload_many_blobs_with_transfer_manager(
            test_bucket.name,
            BLOB_NAMES,
            source_directory="{}/".format(uploads),
            workers=8,
        )
        out, _ = capsys.readouterr()

        for name in BLOB_NAMES:
            assert "Uploaded {}".format(name) in out

    with tempfile.TemporaryDirectory() as downloads:
        # Download the files.
        storage_transfer_manager_download_bucket.download_bucket_with_transfer_manager(
            test_bucket.name,
            destination_directory=os.path.join(downloads, ""),
            workers=8,
            max_results=10000,
        )
        out, _ = capsys.readouterr()

        for name in BLOB_NAMES:
            assert "Downloaded {}".format(name) in out

    with tempfile.TemporaryDirectory() as downloads:
        # Download the files.
        storage_transfer_manager_download_many.download_many_blobs_with_transfer_manager(
            test_bucket.name,
            blob_names=BLOB_NAMES,
            destination_directory=os.path.join(downloads, ""),
            workers=8,
        )
        out, _ = capsys.readouterr()

        for name in BLOB_NAMES:
            assert "Downloaded {}".format(name) in out


def test_transfer_manager_directory_upload(test_bucket, capsys):
    BLOB_NAMES = [
        "dirtest/test.txt",
        "dirtest/test2.txt",
        "dirtest/blobs/test.txt",
        "dirtest/blobs/nesteddir/test.txt",
    ]

    with tempfile.TemporaryDirectory() as uploads:
        # Create dirs and nested dirs
        for name in BLOB_NAMES:
            relpath = os.path.dirname(name)
            os.makedirs(os.path.join(uploads, relpath), exist_ok=True)

        # Create files with nested dirs to exercise directory handling.
        for name in BLOB_NAMES:
            with open(os.path.join(uploads, name), "w") as f:
                f.write(name)

        storage_transfer_manager_upload_directory.upload_directory_with_transfer_manager(
            test_bucket.name, source_directory="{}/".format(uploads)
        )
        out, _ = capsys.readouterr()

        assert "Found {}".format(len(BLOB_NAMES)) in out
        for name in BLOB_NAMES:
            assert "Uploaded {}".format(name) in out


def test_transfer_manager_download_chunks_concurrently(test_bucket, capsys):
    BLOB_NAME = "test_file.txt"

    with tempfile.NamedTemporaryFile() as file:
        file.write(b"test")
        file.flush()

        storage_upload_file.upload_blob(test_bucket.name, file.name, BLOB_NAME)

    with tempfile.TemporaryDirectory() as downloads:
        # Download the file.
        storage_transfer_manager_download_chunks_concurrently.download_chunks_concurrently(
            test_bucket.name,
            BLOB_NAME,
            os.path.join(downloads, BLOB_NAME),
            workers=8,
        )
        out, _ = capsys.readouterr()

        assert (
            "Downloaded {} to {}".format(BLOB_NAME, os.path.join(downloads, BLOB_NAME))
            in out
        )


def test_transfer_manager_upload_chunks_concurrently(test_bucket, capsys):
    BLOB_NAME = "test_file.txt"

    with tempfile.NamedTemporaryFile() as file:
        file.write(b"test")
        file.flush()

        storage_transfer_manager_upload_chunks_concurrently.upload_chunks_concurrently(
            test_bucket.name, file.name, BLOB_NAME
        )

        out, _ = capsys.readouterr()
        assert "File {} uploaded to {}".format(file.name, BLOB_NAME) in out


def test_object_retention_policy(test_bucket_create, capsys):
    storage_create_bucket_object_retention.create_bucket_object_retention(
        test_bucket_create.name
    )
    out, _ = capsys.readouterr()
    assert (
        f"Created bucket {test_bucket_create.name} with object retention enabled setting"
        in out
    )

    blob_name = "test_object_retention"
    storage_set_object_retention_policy.set_object_retention_policy(
        test_bucket_create.name, "hello world", blob_name
    )
    out, _ = capsys.readouterr()
    assert f"Retention policy for file {blob_name}" in out

    # Remove retention policy for test cleanup
    blob = test_bucket_create.blob(blob_name)
    blob.retention.mode = None
    blob.retention.retain_until_time = None
    blob.patch(override_unlocked_retention=True)


def test_create_bucket_hierarchical_namespace(test_bucket_create, capsys):
    storage_create_bucket_hierarchical_namespace.create_bucket_hierarchical_namespace(
        test_bucket_create.name
    )
    out, _ = capsys.readouterr()
    assert (
        f"Created bucket {test_bucket_create.name} with hierarchical namespace enabled"
        in out
    )


def test_storage_trace_quickstart(test_bucket, capsys):
    blob_name = f"trace_quickstart_{uuid.uuid4().hex}"
    contents = "The quick brown fox jumps over the lazy dog."
    storage_trace_quickstart.run_quickstart(test_bucket.name, blob_name, contents)
    out, _ = capsys.readouterr()

    assert f"{blob_name} uploaded to {test_bucket.name}" in out
    assert (
        f"Downloaded storage object {blob_name} from bucket {test_bucket.name}" in out
    )


def test_storage_disable_soft_delete(test_soft_delete_enabled_bucket, capsys):
    bucket_name = test_soft_delete_enabled_bucket.name
    storage_disable_soft_delete.disable_soft_delete(bucket_name)
    out, _ = capsys.readouterr()
    assert f"Soft-delete policy is disabled for bucket {bucket_name}" in out


def test_storage_get_soft_delete_policy(test_soft_delete_enabled_bucket, capsys):
    bucket_name = test_soft_delete_enabled_bucket.name
    storage_get_soft_delete_policy.get_soft_delete_policy(bucket_name)
    out, _ = capsys.readouterr()
    assert f"Soft-delete policy for {bucket_name}" in out
    assert "Object soft-delete policy is enabled" in out
    assert "Object retention duration: " in out
    assert "Policy effective time: " in out

    # Disable the soft-delete policy
    test_soft_delete_enabled_bucket.soft_delete_policy.retention_duration_seconds = 0
    test_soft_delete_enabled_bucket.patch()
    storage_get_soft_delete_policy.get_soft_delete_policy(bucket_name)
    out, _ = capsys.readouterr()
    assert f"Soft-delete policy for {bucket_name}" in out
    assert "Object soft-delete policy is disabled" in out


def test_storage_set_soft_delete_policy(test_soft_delete_enabled_bucket, capsys):
    bucket_name = test_soft_delete_enabled_bucket.name
    retention_duration_seconds = 10 * 24 * 60 * 60  # 10 days
    storage_set_soft_delete_policy.set_soft_delete_policy(
        bucket_name, retention_duration_seconds
    )
    out, _ = capsys.readouterr()
    assert (
        f"Soft delete policy for bucket {bucket_name} was set to {retention_duration_seconds} seconds retention period"
        in out
    )


def test_storage_list_soft_deleted_objects(test_soft_delete_enabled_bucket, capsys):
    bucket_name = test_soft_delete_enabled_bucket.name
    blob_name = f"test_object_{uuid.uuid4().hex}.txt"
    blob_content = "This object will be soft-deleted for listing."
    blob = test_soft_delete_enabled_bucket.blob(blob_name)
    blob.upload_from_string(blob_content)
    blob_generation = blob.generation

    blob.delete()  # Soft-delete the object
    storage_list_soft_deleted_objects.list_soft_deleted_objects(bucket_name)
    out, _ = capsys.readouterr()
    assert f"Name: {blob_name}, Generation: {blob_generation}" in out


def test_storage_list_soft_deleted_object_versions(
    test_soft_delete_enabled_bucket, capsys
):
    bucket_name = test_soft_delete_enabled_bucket.name
    blob_name = f"test_object_{uuid.uuid4().hex}.txt"
    blob_content = "This object will be soft-deleted for version listing."
    blob = test_soft_delete_enabled_bucket.blob(blob_name)
    blob.upload_from_string(blob_content)
    blob_generation = blob.generation

    blob.delete()  # Soft-delete the object
    storage_list_soft_deleted_object_versions.list_soft_deleted_object_versions(
        bucket_name, blob_name
    )
    out, _ = capsys.readouterr()
    assert f"Version ID: {blob_generation}" in out


def test_storage_restore_soft_deleted_object(test_soft_delete_enabled_bucket, capsys):
    bucket_name = test_soft_delete_enabled_bucket.name
    blob_name = f"test-restore-sd-obj-{uuid.uuid4().hex}.txt"
    blob_content = "This object will be soft-deleted and restored."
    blob = test_soft_delete_enabled_bucket.blob(blob_name)
    blob.upload_from_string(blob_content)
    blob_generation = blob.generation

    blob.delete()  # Soft-delete the object
    storage_restore_object.restore_soft_deleted_object(
        bucket_name, blob_name, blob_generation
    )
    out, _ = capsys.readouterr()
    assert (
        f"Soft-deleted object {blob_name} is restored in the bucket {bucket_name}"
        in out
    )

    # Verify the restoration
    blob = test_soft_delete_enabled_bucket.get_blob(blob_name)
    assert blob is not None


def test_move_object(test_blob):
    bucket = test_blob.bucket
    try:
        bucket.delete_blob("test_move_blob_atomic")
    except google.cloud.exceptions.NotFound:
        print(f"test_move_blob_atomic not found in bucket {bucket.name}")

    storage_move_file_atomically.move_object(
        bucket.name,
        test_blob.name,
        "test_move_blob_atomic",
    )

    assert bucket.get_blob("test_move_blob_atomic") is not None
    assert bucket.get_blob(test_blob.name) is None
