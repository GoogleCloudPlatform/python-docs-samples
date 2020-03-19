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

import storage_get_uniform_bucket_level_access
import storage_disable_uniform_bucket_level_access
import storage_enable_uniform_bucket_level_access


@pytest.fixture()
def bucket():
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "uniform-bucket-level-access-{}".format(int(time.time()))
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    time.sleep(3)
    bucket.delete(force=True)


def test_get_uniform_bucket_level_access(bucket, capsys):
    storage_get_uniform_bucket_level_access.get_uniform_bucket_level_access(
        bucket.name
    )
    out, _ = capsys.readouterr()
    assert (
        "Uniform bucket-level access is disabled for {}.".format(bucket.name)
        in out
    )


def test_enable_uniform_bucket_level_access(bucket, capsys):
    short_name = storage_enable_uniform_bucket_level_access
    short_name.enable_uniform_bucket_level_access(
        bucket.name
    )
    out, _ = capsys.readouterr()
    assert (
        "Uniform bucket-level access was enabled for {}.".format(bucket.name)
        in out
    )


def test_disable_uniform_bucket_level_access(bucket, capsys):
    short_name = storage_disable_uniform_bucket_level_access
    short_name.disable_uniform_bucket_level_access(
        bucket.name
    )
    out, _ = capsys.readouterr()
    assert (
        "Uniform bucket-level access was disabled for {}.".format(bucket.name)
        in out
    )
