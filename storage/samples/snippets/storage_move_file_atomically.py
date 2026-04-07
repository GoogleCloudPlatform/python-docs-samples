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

# [START storage_move_object]
from google.cloud import storage


def move_object(bucket_name: str, blob_name: str, new_blob_name: str) -> None:
    """Moves a blob to a new name within the same bucket using the move API."""
    # The name of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The name of your GCS object to move
    # blob_name = "your-file-name"

    # The new name of the GCS object
    # new_blob_name = "new-file-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob_to_move = bucket.blob(blob_name)

    # Use move_blob to perform an efficient, server-side move.
    moved_blob = bucket.move_blob(
        blob=blob_to_move, new_name=new_blob_name
    )

    print(f"Blob {blob_to_move.name} has been moved to {moved_blob.name}.")


# [END storage_move_object]

if __name__ == "__main__":
    move_object(
        bucket_name=sys.argv[1],
        blob_name=sys.argv[2],
        new_blob_name=sys.argv[3],
    )
