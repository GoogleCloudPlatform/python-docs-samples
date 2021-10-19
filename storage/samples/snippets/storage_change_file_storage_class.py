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

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    blob.update_storage_class("NEARLINE")

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
