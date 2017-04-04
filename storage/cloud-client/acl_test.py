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

from google.cloud import storage
import google.cloud.storage.acl
import pytest

import acl

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
# Typically we'd use a @example.com address, but GCS requires a real Google
# account.
TEST_EMAIL = 'jonwayne@google.com'


@pytest.fixture
def test_bucket():
    """Yields a bucket that resets its acl after the test completes."""
    bucket = storage.Client().bucket(BUCKET)
    acl = google.cloud.storage.acl.BucketACL(bucket)
    object_default_acl = google.cloud.storage.acl.DefaultObjectACL(bucket)
    acl.reload()
    object_default_acl.reload()
    yield bucket
    acl.save()
    object_default_acl.save()


@pytest.fixture
def test_blob():
    """Yields a blob that resets its acl after the test completes."""
    bucket = storage.Client().bucket(BUCKET)
    blob = bucket.blob('storage_acl_test_sigil')
    blob.upload_from_string('Hello, is it me you\'re looking for?')
    acl = google.cloud.storage.acl.ObjectACL(blob)
    acl.reload()
    yield blob
    acl.save()


def test_print_bucket_acl(capsys):
    acl.print_bucket_acl(BUCKET)
    out, _ = capsys.readouterr()
    assert out


def test_print_bucket_acl_for_user(test_bucket, capsys):
    test_bucket.acl.user(TEST_EMAIL).grant_owner()
    test_bucket.acl.save()

    acl.print_bucket_acl_for_user(BUCKET, TEST_EMAIL)

    out, _ = capsys.readouterr()
    assert 'OWNER' in out


def test_add_bucket_owner(test_bucket):
    acl.add_bucket_owner(BUCKET, TEST_EMAIL)

    test_bucket.acl.reload()
    assert 'OWNER' in test_bucket.acl.user(TEST_EMAIL).get_roles()


def test_remove_bucket_owner(test_bucket):
    test_bucket.acl.user(TEST_EMAIL).grant_owner()
    test_bucket.acl.save()

    acl.remove_bucket_owner(BUCKET, TEST_EMAIL)

    test_bucket.acl.reload()
    assert 'OWNER' not in test_bucket.acl.user(TEST_EMAIL).get_roles()


def test_add_bucket_default_owner(test_bucket):
    acl.add_bucket_default_owner(BUCKET, TEST_EMAIL)

    test_bucket.default_object_acl.reload()
    roles = test_bucket.default_object_acl.user(TEST_EMAIL).get_roles()
    assert 'OWNER' in roles


def test_remove_bucket_default_owner(test_bucket):
    test_bucket.acl.user(TEST_EMAIL).grant_owner()
    test_bucket.acl.save()

    acl.remove_bucket_default_owner(BUCKET, TEST_EMAIL)

    test_bucket.default_object_acl.reload()
    roles = test_bucket.default_object_acl.user(TEST_EMAIL).get_roles()
    assert 'OWNER' not in roles


def test_print_blob_acl(test_blob, capsys):
    acl.print_blob_acl(BUCKET, test_blob.name)
    out, _ = capsys.readouterr()
    assert out


def test_print_blob_acl_for_user(test_blob, capsys):
    test_blob.acl.user(TEST_EMAIL).grant_owner()
    test_blob.acl.save()

    acl.print_blob_acl_for_user(
        BUCKET, test_blob.name, TEST_EMAIL)

    out, _ = capsys.readouterr()
    assert 'OWNER' in out


def test_add_blob_owner(test_blob):
    acl.add_blob_owner(BUCKET, test_blob.name, TEST_EMAIL)

    test_blob.acl.reload()
    assert 'OWNER' in test_blob.acl.user(TEST_EMAIL).get_roles()


def test_remove_blob_owner(test_blob):
    test_blob.acl.user(TEST_EMAIL).grant_owner()
    test_blob.acl.save()

    acl.remove_blob_owner(
        BUCKET, test_blob.name, TEST_EMAIL)

    test_blob.acl.reload()
    assert 'OWNER' not in test_blob.acl.user(TEST_EMAIL).get_roles()
