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
import uuid

from google.cloud import storage
import pytest

import storage_disable_default_event_based_hold
import storage_enable_default_event_based_hold
import storage_get_default_event_based_hold
import storage_get_retention_policy
import storage_lock_retention_policy
import storage_release_event_based_hold
import storage_release_temporary_hold
import storage_remove_retention_policy
import storage_set_event_based_hold
import storage_set_retention_policy
import storage_set_temporary_hold


BLOB_NAME = "storage_snippets_test_sigil"
BLOB_CONTENT = "Hello, is it me you're looking for?"
# Retention policy for 5 seconds
RETENTION_POLICY = 5


@pytest.fixture
def bucket():
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "bucket-lock-{}".format(uuid.uuid4())
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    bucket.delete(force=True)


def test_retention_policy_no_lock(bucket, capsys):
    storage_set_retention_policy.set_retention_policy(
        bucket.name, RETENTION_POLICY
    )
    bucket.reload()

    assert bucket.retention_period is RETENTION_POLICY
    assert bucket.retention_policy_effective_time is not None
    assert bucket.retention_policy_locked is None

    storage_get_retention_policy.get_retention_policy(bucket.name)
    out, _ = capsys.readouterr()
    assert "Retention Policy for {}".format(bucket.name) in out
    assert "Retention Period: 5" in out
    assert "Effective Time: " in out
    assert "Retention Policy is locked" not in out

    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)

    assert blob.retention_expiration_time is not None

    storage_remove_retention_policy.remove_retention_policy(bucket.name)
    bucket.reload()
    assert bucket.retention_period is None

    time.sleep(RETENTION_POLICY)


def test_retention_policy_lock(bucket, capsys):
    storage_set_retention_policy.set_retention_policy(
        bucket.name, RETENTION_POLICY
    )
    bucket.reload()
    assert bucket.retention_policy_locked is None

    storage_lock_retention_policy.lock_retention_policy(bucket.name)
    bucket.reload()
    assert bucket.retention_policy_locked is True

    storage_get_retention_policy.get_retention_policy(bucket.name)
    out, _ = capsys.readouterr()
    assert "Retention Policy is locked" in out


def test_enable_disable_bucket_default_event_based_hold(bucket, capsys):
    storage_get_default_event_based_hold.get_default_event_based_hold(
        bucket.name
    )
    out, _ = capsys.readouterr()
    assert (
        "Default event-based hold is not enabled for {}".format(bucket.name)
        in out
    )
    assert (
        "Default event-based hold is enabled for {}".format(bucket.name)
        not in out
    )

    storage_enable_default_event_based_hold.enable_default_event_based_hold(
        bucket.name
    )
    bucket.reload()

    assert bucket.default_event_based_hold is True

    storage_get_default_event_based_hold.get_default_event_based_hold(
        bucket.name
    )
    out, _ = capsys.readouterr()
    assert (
        "Default event-based hold is enabled for {}".format(bucket.name) in out
    )

    # Changes to the bucket will be readable immediately after writing,
    # but configuration changes may take time to propagate.
    time.sleep(10)

    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.event_based_hold is True

    storage_release_event_based_hold.release_event_based_hold(
        bucket.name, blob.name
    )
    blob.reload()
    assert blob.event_based_hold is False

    storage_disable_default_event_based_hold.disable_default_event_based_hold(
        bucket.name
    )
    bucket.reload()
    assert bucket.default_event_based_hold is False


def test_enable_disable_temporary_hold(bucket):
    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.temporary_hold is None

    storage_set_temporary_hold.set_temporary_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.temporary_hold is True

    storage_release_temporary_hold.release_temporary_hold(
        bucket.name, blob.name
    )
    blob.reload()
    assert blob.temporary_hold is False


def test_enable_disable_event_based_hold(bucket):
    blob = bucket.blob(BLOB_NAME)
    blob.upload_from_string(BLOB_CONTENT)
    assert blob.event_based_hold is None

    storage_set_event_based_hold.set_event_based_hold(bucket.name, blob.name)
    blob.reload()
    assert blob.event_based_hold is True

    storage_release_event_based_hold.release_event_based_hold(
        bucket.name, blob.name
    )
    blob.reload()
    assert blob.event_based_hold is False
