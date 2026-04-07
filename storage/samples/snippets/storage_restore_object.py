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

# [START storage_restore_object]
from google.cloud import storage


def restore_soft_deleted_object(bucket_name, blob_name, blob_generation):
    """Restores a soft-deleted object in the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # blob_generation = "your-object-version-id"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Restore function will override if a live object already
    # exists with the same name.
    bucket.restore_blob(blob_name, generation=blob_generation)

    print(
        f"Soft-deleted object {blob_name} is restored in the bucket {bucket_name}"
    )


# [END storage_restore_object]

if __name__ == "__main__":
    restore_soft_deleted_object(
        bucket_name=sys.argv[1], blob_name=sys.argv[2], blob_generation=sys.argv[3]
    )
