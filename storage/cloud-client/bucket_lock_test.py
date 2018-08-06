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

import os
import pytest

import bucket_lock

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
# Retention policy for one week
RETENTION_POLICY = 60 * 60 * 24 * 7


@pytest.fixture
def test_blob():
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage.Client().bucket(BUCKET)
    blob = bucket.blob('storage_snippets_test_sigil')
    blob.upload_from_string('Hello, is it me you\'re looking for?')
    return blob


def test_set_retention_policy(capsys):
    bucket_lock.set_retention_policy(BUCKET, RETENTION_POLICY)
    out, _ = capsys.readouterr()
    assert out


def test_remove_retention_policy(capsys):
    bucket_lock.remove_retention_policy(BUCKET)
    out, _ = capsys.readouterr()
    assert out


def test_lock_retention_policy(capsys):
    bucket_lock.lock_retention_policy(BUCKET)
    out, _ = capsys.readouterr()
    assert out


def test_set_temporary_hold(capsys):
    bucket_lock.set_temporary_hold(BUCKET, 'storage_snippets_test_sigil')
    out, _ = capsys.readouterr()
    assert out


def test_release_temporary_hold(capsys):
    bucket_lock.release_temporary_hold(BUCKET, 'storage_snippets_test_sigil')
    out, _ = capsys.readouterr()
    assert out

def test_set_event_based_hold(capsys):
    bucket_lock.set_event_based_hold(BUCKET, 'storage_snippets_test_sigil')
    out, _ = capsys.readouterr()
    assert out


def test_release_event_based_hold(capsys):
    bucket_lock.release_event_based_hold(BUCKET, 'storage_snippets_test_sigil')
    out, _ = capsys.readouterr()
    assert out


def test_enable_default_event_based_hold(capsys):
    bucket_lock.enable_default_event_based_hold(BUCKET)
    out, _ = capsys.readouterr()
    assert out


def test_disable_default_event_based_hold(capsys):
    bucket_lock.disable_default_event_based_hold(BUCKET)
    out, _ = capsys.readouterr()
    assert out
