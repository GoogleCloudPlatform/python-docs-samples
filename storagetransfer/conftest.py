# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Useful utilities for STS samples tests.
"""

import os
import uuid

from google.cloud import storage, storage_transfer

import pytest


@pytest.fixture(scope='module')
def project_id():
    yield os.environ.get("GOOGLE_CLOUD_PROJECT")


@pytest.fixture(scope='module')
def bucket_name():
    yield f"sts-python-samples-test-{uuid.uuid4()}"


@pytest.fixture(scope='module')
def sts_service_account(project_id):
    client = storage_transfer.StorageTransferServiceClient()
    account = client.get_google_service_account({'project_id': project_id})

    yield account.account_email


@pytest.fixture(scope='module')
def aws_source_bucket(bucket_name: str):
    # TODO:
    # s3 = AmazonS3ClientBuilder.standard().withRegion(Regions.US_WEST_1)

    # s3.createBucket(AMAZON_BUCKET);

    pass

    # s3.deleteBucket(AMAZON_BUCKET);


@pytest.fixture(scope='module')
def gcs_bucket(project_id: str, bucket_name: str):
    """
    Yields and auto-cleans up a CGS bucket for use in STS jobs
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete()


@pytest.fixture(scope='module')
def source_bucket(gcs_bucket: storage.Bucket, sts_service_account: str):
    """
    Yields and auto-cleans up a CGS bucket preconfigured with necessary
    STS service account read perms
    """

    # Setup policy for STS
    member: str = f"serviceAccount:{sts_service_account}"
    objectViewer = "roles/storage.objectViewer"
    bucketReader = "roles/storage.legacyBucketReader"

    # Prepare policy
    policy = gcs_bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": objectViewer, "members": {member}})
    policy.bindings.append({"role": bucketReader, "members": {member}})

    # Set policy
    gcs_bucket.set_iam_policy(policy)

    yield gcs_bucket


@pytest.fixture(scope='module')
def destination_bucket(gcs_bucket: storage.Bucket, sts_service_account: str):
    """
    Yields and auto-cleans up a CGS bucket preconfigured with necessary
    STS service account write perms
    """

    # Setup policy for STS
    member: str = f"serviceAccount:{sts_service_account}"
    bucketWriter = "roles/storage.legacyBucketWriter"

    # Prepare policy
    policy = gcs_bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": bucketWriter, "members": {member}})

    # Set policy
    gcs_bucket.set_iam_policy(policy)

    yield gcs_bucket
