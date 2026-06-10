# Copyright 2026 Google LLC
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

from google.cloud import storage

import pytest

import create_folder
import delete_folder_recursive


def test_delete_folder_recursive(
    capsys: pytest.LogCaptureFixture, hns_enabled_bucket: storage.Bucket, uuid_name: str
) -> None:
    bucket_name = hns_enabled_bucket.name
    folder_name = uuid_name

    # Create a folder
    create_folder.create_folder(bucket_name=bucket_name, folder_name=folder_name)

    # Create an object inside the folder so that recursive delete is required
    blob = hns_enabled_bucket.blob(f"{folder_name}/test.txt")
    blob.upload_from_string("test data")

    # Delete folder recursively
    delete_folder_recursive.delete_folder_recursive(
        bucket_name=bucket_name, folder_name=folder_name
    )

    out, _ = capsys.readouterr()
    assert folder_name in out

    # Verify the object is deleted
    assert not blob.exists()
