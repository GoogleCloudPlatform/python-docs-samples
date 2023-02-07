#!/usr/bin/env python

# Copyright 2020 Google LLC. All Rights Reserved.
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

# [START storage_change_file_storage_class]
from google.cloud import storage


def change_file_storage_class(bucket_name, blob_name):
    """Change the default storage class of the blob"""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None

    # Optional: set a generation-match precondition to avoid potential race
    # conditions and data corruptions. The request is aborted if the
    # object's generation number does not match your precondition.
    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.update_storage_class("NEARLINE", if_generation_match=generation_match_precondition)

    print(
        "Blob {} in bucket {} had its storage class set to {}".format(
            blob_name,
            bucket_name,
            blob.storage_class
        )
    )
    return blob
# [END storage_change_file_storage_class]


if __name__ == "__main__":
    change_file_storage_class(bucket_name=sys.argv[1], blob_name=sys.argv[2])
