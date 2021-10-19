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
import uuid

import backoff
from google.cloud import storage
from googleapiclient.errors import HttpError
import pytest

import storage_add_bucket_default_owner
import storage_add_bucket_owner
import storage_add_file_owner
import storage_print_bucket_acl
import storage_print_bucket_acl_for_user
import storage_print_file_acl
import storage_print_file_acl_for_user
import storage_remove_bucket_default_owner
import storage_remove_bucket_owner
import storage_remove_file_owner

# Typically we'd use a @example.com address, but GCS requires a real Google
# account. Retrieve a service account email with storage admin permissions.
TEST_EMAIL = (
    "py38-storage-test"
    "@python-docs-samples-tests.iam.gserviceaccount.com"
)


@pytest.fixture(scope="module")
def test_bucket():
    """Yields a bucket that is deleted after the test completes."""

    # The new projects have uniform bucket-level access and our tests don't
    # pass with those buckets. We need to use the old main project for now.
    original_value = os.environ['GOOGLE_CLOUD_PROJECT']
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['MAIN_GOOGLE_CLOUD_PROJECT']
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "acl-test-{}".format(uuid.uuid4())
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    bucket.delete(force=True)
    # Set the value back.
    os.environ['GOOGLE_CLOUD_PROJECT'] = original_value


@pytest.fixture
def test_blob(test_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_bucket
    blob = bucket.blob("storage_acl_test_sigil-{}".format(uuid.uuid4()))
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


def test_print_bucket_acl(test_bucket, capsys):
    storage_print_bucket_acl.print_bucket_acl(test_bucket.name)
    out, _ = capsys.readouterr()
    assert out


def test_print_bucket_acl_for_user(test_bucket, capsys):
    test_bucket.acl.user(TEST_EMAIL).grant_owner()
    test_bucket.acl.save()

    storage_print_bucket_acl_for_user.print_bucket_acl_for_user(
        test_bucket.name, TEST_EMAIL
    )

    out, _ = capsys.readouterr()
    assert "OWNER" in out


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_add_bucket_owner(test_bucket):
    storage_add_bucket_owner.add_bucket_owner(test_bucket.name, TEST_EMAIL)

    test_bucket.acl.reload()
    assert "OWNER" in test_bucket.acl.user(TEST_EMAIL).get_roles()


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_remove_bucket_owner(test_bucket):
    test_bucket.acl.user(TEST_EMAIL).grant_owner()
    test_bucket.acl.save()

    storage_remove_bucket_owner.remove_bucket_owner(
        test_bucket.name, TEST_EMAIL)

    test_bucket.acl.reload()
    assert "OWNER" not in test_bucket.acl.user(TEST_EMAIL).get_roles()


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_add_bucket_default_owner(test_bucket):
    storage_add_bucket_default_owner.add_bucket_default_owner(
        test_bucket.name, TEST_EMAIL
    )

    test_bucket.default_object_acl.reload()
    roles = test_bucket.default_object_acl.user(TEST_EMAIL).get_roles()
    assert "OWNER" in roles


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_remove_bucket_default_owner(test_bucket):
    test_bucket.acl.user(TEST_EMAIL).grant_owner()
    test_bucket.acl.save()

    storage_remove_bucket_default_owner.remove_bucket_default_owner(
        test_bucket.name, TEST_EMAIL
    )

    test_bucket.default_object_acl.reload()
    roles = test_bucket.default_object_acl.user(TEST_EMAIL).get_roles()
    assert "OWNER" not in roles


def test_print_blob_acl(test_blob, capsys):
    storage_print_file_acl.print_blob_acl(
        test_blob.bucket.name, test_blob.name)
    out, _ = capsys.readouterr()
    assert out


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_print_blob_acl_for_user(test_blob, capsys):
    test_blob.acl.user(TEST_EMAIL).grant_owner()
    test_blob.acl.save()

    storage_print_file_acl_for_user.print_blob_acl_for_user(
        test_blob.bucket.name, test_blob.name, TEST_EMAIL
    )

    out, _ = capsys.readouterr()
    assert "OWNER" in out


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_add_blob_owner(test_blob):
    storage_add_file_owner.add_blob_owner(
        test_blob.bucket.name, test_blob.name, TEST_EMAIL)

    test_blob.acl.reload()
    assert "OWNER" in test_blob.acl.user(TEST_EMAIL).get_roles()


@backoff.on_exception(backoff.expo, HttpError, max_time=60)
def test_remove_blob_owner(test_blob):
    test_blob.acl.user(TEST_EMAIL).grant_owner()
    test_blob.acl.save()

    storage_remove_file_owner.remove_blob_owner(
        test_blob.bucket.name, test_blob.name, TEST_EMAIL
    )

    test_blob.acl.reload()
    assert "OWNER" not in test_blob.acl.user(TEST_EMAIL).get_roles()
