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

import uuid

from google.cloud import storage

import pytest

import managed_folder_create
import managed_folder_delete

# NOTE(reviewers): Managed Folder module would require a whole set of tests
# to create the folder, get it, and finally destroying it.
# See an example in snippets_test.py of the whole use case.


def test_storage_control_managed_folder_list(
    capsys: pytest.LogCaptureFixture, gcs_bucket: storage.Bucket
) -> None:
    bucket_name = gcs_bucket.name
    # Follow the naming requirements:
    # https://cloud.google.com/storage/docs/buckets#naming
    managed_folder_name = "create_managed_folder_" + str(uuid.uuid4())

    managed_folder_create.create_managed_folder(
        bucket_name=bucket_name,
        managed_folder_name=managed_folder_name
    )

    out, _ = capsys.readouterr()
    folder_resource_name = (
        f"projects/_/buckets/{bucket_name}/managedFolders/{managed_folder_name}/"
    )
    assert folder_resource_name in out

    # Cleanup
    managed_folder_delete.delete_managed_folder(
        bucket_name=bucket_name,
        managed_folder_id=managed_folder_name
    )
