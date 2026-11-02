# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import uuid

from google.api_core import exceptions
from google.api_core import retry
from google.cloud import storage

import pytest


@pytest.fixture(scope="module")
def project_id() -> str:
    yield os.environ.get("BUILD_SPECIFIC_GCLOUD_PROJECT")


@pytest.fixture(scope="function")
def uuid_name(prefix: str = "storagecontrol") -> str:
    yield f"{prefix}-{uuid.uuid4().hex[:5]}"


@pytest.fixture(scope="function")
def bucket_name() -> str:
    yield f"storagecontrol-samples-{uuid.uuid4()}"


@pytest.fixture(scope="function")
def gcs_bucket(project_id: str, bucket_name: str) -> storage.Bucket:
    """
    Yields and auto-cleans up a GCS bucket for use in Storage Control quickstart
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


@pytest.fixture(scope="function")
def hns_enabled_bucket(project_id: str, bucket_name: str) -> storage.Bucket:
    """
    Yields and auto-cleans up an HNS enabled bucket.
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.hierarchical_namespace_enabled = True
    bucket = storage_client.create_bucket(bucket)

    yield bucket

    bucket.delete(force=True)


@pytest.fixture(scope="module")
def rapid_cache_zone() -> str:
    yield os.environ.get("RAPID_CACHE_ZONE", "us-central1-a")


@pytest.fixture(scope="function")
def regional_hns_enabled_bucket(
    project_id: str, bucket_name: str, rapid_cache_zone: str
) -> storage.Bucket:
    """
    Yields and auto-cleans up a regional HNS enabled bucket located in the
    region of the Rapid Cache zone.
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.hierarchical_namespace_enabled = True
    region = rapid_cache_zone.rsplit("-", 1)[0]
    bucket = storage_client.create_bucket(bucket, location=region)

    yield bucket

    # A bucket cannot be deleted until its disabled Rapid Cache has been fully
    # removed, which can take more than 30 minutes. Cleanup is best-effort: a
    # short retry, after which the bucket is left behind for later cleanup.
    try:
        retry.Retry(
            predicate=retry.if_exception_type(exceptions.Conflict),
            initial=10.0,
            maximum=30.0,
            timeout=120.0,
        )(bucket.delete)(force=True)
    except exceptions.GoogleAPIError as e:
        logging.warning("Could not delete bucket %s: %s", bucket.name, e)


@pytest.fixture(scope="function")
def ubla_enabled_bucket(project_id: str, bucket_name: str) -> storage.Bucket:
    """
    Yields and auto-cleans up an UBLA enabled bucket.
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket = storage_client.create_bucket(bucket)

    yield bucket

    bucket.delete(force=True)
