# Copyright 2017 Google, Inc.
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
import pytest

import iam

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
MEMBER = 'group:dpebot@google.com'
ROLE = 'roles/storage.legacyBucketReader'


@pytest.fixture
def bucket():
    yield storage.Client().bucket(BUCKET)


def test_view_bucket_iam_members():
    iam.view_bucket_iam_members(BUCKET)


def test_add_bucket_iam_member(bucket):
    iam.add_bucket_iam_member(
        BUCKET, ROLE, MEMBER)
    assert MEMBER in bucket.get_iam_policy()[ROLE]


def test_remove_bucket_iam_member(bucket):
    iam.remove_bucket_iam_member(
        BUCKET, ROLE, MEMBER)
    assert MEMBER not in bucket.get_iam_policy()[ROLE]
