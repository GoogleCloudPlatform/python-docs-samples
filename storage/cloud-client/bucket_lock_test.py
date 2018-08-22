# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

import google.api_core.exceptions
from google.cloud import storage

import pytest

import bucket_lock

BLOB_NAME = 'storage_snippets_test_sigil'
BLOB_CONTENT = 'Hello, is it me you\'re looking for?'
# Retention policy for 5 seconds
RETENTION_POLICY = 5


@pytest.fixture()
def bucket():
    """Creates a test bucket and deletes it upon completion."""
    client = storage.Client()
    bucket_name = 'bucket-lock-' + str(int(time.time()))
    bucket = client.create_bucket(bucket_name)
    yield bucket
    bucket.delete(force=True)


def test_retention_policy_no_lock(bucket):
    bucket_lock.set_retention_policy(bucket.name, RETENTION_POLICY)
    bucket.reload()

    assert bucket.retention_period is RETENTION_POLICY
    assert bucket.retention_policy_effective_time is not None
    assert bucket.retention_policy_locked is None

    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)

    assert blob.retention_expiration_time is not None

    bucket_lock.remove_retention_policy(bucket.name)
    bucket.reload()
    assert bucket.retention_period is None

    time.sleep(RETENTION_POLICY)


def test_retention_policy_lock(bucket):
    bucket_lock.set_retention_policy(bucket.name, RETENTION_POLICY)
    bucket.reload()
    assert bucket.retention_policy_locked is None

    bucket_lock.lock_retention_policy(bucket.name)
    bucket.reload()
    assert bucket.retention_policy_locked is True

    time.sleep(RETENTION_POLICY)


def test_attempt_object_delete_with_retention_policy(bucket):
    bucket_lock.set_retention_policy(bucket.name, RETENTION_POLICY)
    bucket.reload()

    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.retention_expiration_time is not None

    with pytest.raises(google.api_core.exceptions.Forbidden) as e:
        blob.delete()
        expected = 'is subject to bucket\'s retention policy and cannot be ' \
                   'deleted, overwritten or archived until'
        assert expected in e.message

    time.sleep(RETENTION_POLICY)


def test_enable_disable_bucket_default_event_based_hold(bucket):
    bucket_lock.enable_default_event_based_hold(bucket.name)
    bucket.reload()

    assert bucket.default_event_based_hold is True

    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.event_based_hold is True

    bucket_lock.release_event_based_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.event_based_hold is False

    bucket_lock.disable_default_event_based_hold(bucket.name)
    bucket.reload()
    assert bucket.default_event_based_hold is False


def test_enable_disable_temporary_hold(bucket):
    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.temporary_hold is None

    bucket_lock.set_temporary_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.temporary_hold is True

    bucket_lock.release_temporary_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.temporary_hold is False


def test_attempt_object_delete_with_event_based_hold(bucket):
    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.event_based_hold is None

    bucket_lock.set_event_based_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.event_based_hold is True

    with pytest.raises(google.api_core.exceptions.Forbidden) as e:
        blob.delete()
        expected = 'is under active Event-Based hold and cannot be ' \
                   'deleted, overwritten or archived until hold is removed.'
        assert expected in e.message

    bucket_lock.release_event_based_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.event_based_hold is False


def test_attempt_object_delete_with_temporary_hold(bucket):
    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.temporary_hold is None

    bucket_lock.set_temporary_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.temporary_hold is True

    with pytest.raises(google.api_core.exceptions.Forbidden) as e:
        blob.delete()
        expected = 'is under active Event-Based hold and cannot be ' \
                   'deleted, overwritten or archived until hold is removed.'
        assert expected in e.message

    bucket_lock.release_temporary_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.temporary_hold is False
