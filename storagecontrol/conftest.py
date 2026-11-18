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

import os
import uuid

from google.api_core import exceptions
from google.cloud import storage
from google.cloud import storage_control_v2

import pytest

import logging


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
    zone = os.environ.get("RAPID_CACHE_ZONE", "").strip() or "us-central1-a"
    parts = zone.split("-")
    if len(parts) < 3 or not all(parts):
        raise ValueError(
            f"Invalid RAPID_CACHE_ZONE {zone!r}; expected a zone like "
            "'us-central1-a'."
        )
    yield zone


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
    # removed, which can take more than an hour. Cleanup is best-effort; if
    # deletion fails with Conflict, leave the bucket for later cleanup.
    try:
        bucket.delete(force=True)
    except exceptions.GoogleAPIError as e:
        logging.warning("Could not delete bucket %s: %s", bucket.name, e)


@pytest.fixture(scope="function")
def rapid_cache_id(
    regional_hns_enabled_bucket: storage.Bucket, rapid_cache_zone: str
) -> str:
    """
    Yields the ID of a Rapid Cache for the regional HNS enabled bucket. If the
    test created the Rapid Cache and left it active, it is disabled on
    teardown so that the bucket can be deleted once the cache is removed.
    """

    # The ID of the Rapid Cache. This test uses the zone as the cache ID.
    cache_id = rapid_cache_zone

    yield cache_id

    storage_control_client = storage_control_v2.StorageControlClient()
    bucket_path = (
        f"{storage_control_client.common_project_path('_')}"
        f"/buckets/{regional_hns_enabled_bucket.name}"
    )
    # Cleanup is best-effort: errors are logged instead of failing the test.
    try:
        for cache in storage_control_client.list_rapid_caches(parent=bucket_path):
            if cache.state != "disabled":
                # Disabling is a long-running operation that completes only once
                # the cache is fully removed, so teardown does not wait for it.
                storage_control_client.disable_rapid_cache(name=cache.name)
    except exceptions.GoogleAPIError as e:
        logging.warning(
            "Could not disable Rapid Cache in bucket %s: %s",
            regional_hns_enabled_bucket.name,
            e,
        )


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
