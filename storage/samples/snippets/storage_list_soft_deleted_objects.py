#!/usr/bin/env python

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

import sys

# [START storage_list_soft_deleted_objects]
from google.cloud import storage


def list_soft_deleted_objects(bucket_name):
    """Lists all soft-deleted objects in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, soft_deleted=True)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(
            f"Name: {blob.name}, Generation: {blob.generation}, Soft Delete Time: {blob.soft_delete_time}"
        )


# [END storage_list_soft_deleted_objects]

if __name__ == "__main__":
    list_soft_deleted_objects(bucket_name=sys.argv[1])
