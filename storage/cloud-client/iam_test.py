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
import re
import time
import uuid

from google.cloud import storage
import pytest

import storage_add_bucket_conditional_iam_binding
import storage_add_bucket_iam_member
import storage_remove_bucket_conditional_iam_binding
import storage_remove_bucket_iam_member
import storage_set_bucket_public_iam
import storage_view_bucket_iam_members

MEMBER = "group:dpebot@google.com"
ROLE = "roles/storage.legacyBucketReader"

CONDITION_TITLE = "match-prefix"
CONDITION_DESCRIPTION = "Applies to objects matching a prefix"
CONDITION_EXPRESSION = (
    'resource.name.startsWith("projects/_/buckets/bucket-name/objects/prefix-a-")'
)


@pytest.fixture(scope="module")
def bucket():
    bucket = None
    while bucket is None or bucket.exists():
        storage_client = storage.Client()
        bucket_name = "test-iam-{}".format(uuid.uuid4())
        bucket = storage_client.bucket(bucket_name)
        bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    storage_client.create_bucket(bucket)
    yield bucket
    time.sleep(3)
    bucket.delete(force=True)


@pytest.fixture(scope="function")
def public_bucket():
    # The new projects don't allow to make a bucket available to public, so
    # we need to use the old main project for now.
    original_value = os.environ['GOOGLE_CLOUD_PROJECT']
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['MAIN_GOOGLE_CLOUD_PROJECT']
    bucket = None
    while bucket is None or bucket.exists():
        storage_client = storage.Client()
        bucket_name = "test-iam-{}".format(uuid.uuid4())
        bucket = storage_client.bucket(bucket_name)
        bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    storage_client.create_bucket(bucket)
    yield bucket
    time.sleep(3)
    bucket.delete(force=True)
    # Set the value back.
    os.environ['GOOGLE_CLOUD_PROJECT'] = original_value


def test_view_bucket_iam_members(capsys, bucket):
    storage_view_bucket_iam_members.view_bucket_iam_members(bucket.name)
    assert re.match("Role: .*, Members: .*", capsys.readouterr().out)


def test_add_bucket_iam_member(bucket):
    storage_add_bucket_iam_member.add_bucket_iam_member(bucket.name, ROLE, MEMBER)
    policy = bucket.get_iam_policy(requested_policy_version=3)
    assert any(
        binding["role"] == ROLE and MEMBER in binding["members"]
        for binding in policy.bindings
    )


def test_add_bucket_conditional_iam_binding(bucket):
    storage_add_bucket_conditional_iam_binding.add_bucket_conditional_iam_binding(
        bucket.name,
        ROLE,
        CONDITION_TITLE,
        CONDITION_DESCRIPTION,
        CONDITION_EXPRESSION,
        {MEMBER},
    )
    policy = bucket.get_iam_policy(requested_policy_version=3)
    assert any(
        binding["role"] == ROLE
        and binding["members"] == {MEMBER}
        and binding["condition"]
        == {
            "title": CONDITION_TITLE,
            "description": CONDITION_DESCRIPTION,
            "expression": CONDITION_EXPRESSION,
        }
        for binding in policy.bindings
    )


def test_remove_bucket_iam_member(public_bucket):
    storage_remove_bucket_iam_member.remove_bucket_iam_member(
        public_bucket.name, ROLE, MEMBER)

    policy = public_bucket.get_iam_policy(requested_policy_version=3)
    assert not any(
        binding["role"] == ROLE and MEMBER in binding["members"]
        for binding in policy.bindings
    )


def test_remove_bucket_conditional_iam_binding(bucket):
    storage_remove_bucket_conditional_iam_binding.remove_bucket_conditional_iam_binding(
        bucket.name, ROLE, CONDITION_TITLE, CONDITION_DESCRIPTION, CONDITION_EXPRESSION
    )

    policy = bucket.get_iam_policy(requested_policy_version=3)
    condition = {
        "title": CONDITION_TITLE,
        "description": CONDITION_DESCRIPTION,
        "expression": CONDITION_EXPRESSION,
    }
    assert not any(
        (binding["role"] == ROLE and binding.get("condition") == condition)
        for binding in policy.bindings
    )


def test_set_bucket_public_iam(public_bucket):
    storage_set_bucket_public_iam.set_bucket_public_iam(public_bucket.name)
    policy = public_bucket.get_iam_policy(requested_policy_version=3)
    assert any(
        binding["role"] == "roles/storage.objectViewer"
        and "allUsers" in binding["members"]
        for binding in policy.bindings
    )
