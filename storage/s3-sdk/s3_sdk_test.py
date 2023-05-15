# Copyright 2021 Google, Inc.
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
from botocore.exceptions import ClientError
from google.cloud import storage
import pytest

import list_gcs_buckets
import list_gcs_objects


PROJECT_ID = os.environ["MAIN_GOOGLE_CLOUD_PROJECT"]
SERVICE_ACCOUNT_EMAIL = os.environ["HMAC_KEY_TEST_SERVICE_ACCOUNT"]
STORAGE_CLIENT = storage.Client(project=PROJECT_ID)


@pytest.fixture(scope="module")
def hmac_fixture():
    """
    Creates an HMAC Key and secret to supply to the S3 SDK tests. The key
    will be deleted after the test session.
    """
    hmac_key, secret = STORAGE_CLIENT.create_hmac_key(
        service_account_email=SERVICE_ACCOUNT_EMAIL, project_id=PROJECT_ID
    )
    yield hmac_key, secret
    hmac_key.state = "INACTIVE"
    hmac_key.update()
    hmac_key.delete()


@pytest.fixture(scope="module")
def test_bucket():
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "bucket-storage-s3-test-{}".format(uuid.uuid4())
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    bucket.delete(force=True)


@pytest.fixture(scope="module")
def test_blob(test_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_bucket
    blob = bucket.blob("storage_snippets_test_sigil-{}".format(uuid.uuid4()))
    blob.upload_from_string("Hello, is it me you're looking for?")
    yield blob


# Retry request because the created key may not be fully propagated for up
# to 15s.
@backoff.on_exception(backoff.constant, ClientError, interval=1, max_time=15)
def test_list_buckets(capsys, hmac_fixture, test_bucket):
    results = list_gcs_buckets.list_gcs_buckets(
        google_access_key_id=hmac_fixture[0].access_id,
        google_access_key_secret=hmac_fixture[1],
    )
    assert test_bucket.name in results


# Retry request because the created key may not be fully propagated for up
# to 15s.
@backoff.on_exception(backoff.constant, ClientError, interval=1, max_time=15)
def test_list_blobs(capsys, hmac_fixture, test_bucket, test_blob):
    result = list_gcs_objects.list_gcs_objects(
        google_access_key_id=hmac_fixture[0].access_id,
        google_access_key_secret=hmac_fixture[1],
        bucket_name=test_bucket.name,
    )
    test_blob.name in result
