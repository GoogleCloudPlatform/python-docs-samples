# Copyright 2019 Google Inc. All Rights Reserved.
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

from google.cloud import storage

import pytest

import bucket_policy_only


@pytest.fixture()
def bucket():
    """Creates a test bucket and deletes it upon completion."""
    client = storage.Client()
    bucket_name = 'bucket-policy-only-' + str(int(time.time()))
    bucket = client.create_bucket(bucket_name)
    yield bucket
    time.sleep(3)
    bucket.delete(force=True)


def test_get_bucket_policy_only(bucket, capsys):
    bucket_policy_only.get_bucket_policy_only(bucket.name)
    out, _ = capsys.readouterr()
    assert 'Bucket Policy Only is disabled for {}.'.format(
        bucket.name) in out


def test_enable_bucket_policy_only(bucket, capsys):
    bucket_policy_only.enable_bucket_policy_only(bucket.name)
    out, _ = capsys.readouterr()
    assert 'Bucket Policy Only was enabled for {}.'.format(
        bucket.name) in out


def test_disable_bucket_policy_only(bucket, capsys):
    bucket_policy_only.disable_bucket_policy_only(bucket.name)
    out, _ = capsys.readouterr()
    assert 'Bucket Policy Only was disabled for {}.'.format(
        bucket.name) in out
