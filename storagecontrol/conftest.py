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
