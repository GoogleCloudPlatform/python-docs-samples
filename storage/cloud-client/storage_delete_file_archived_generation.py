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

# [START storage_delete_file_archived_generation]
from google.cloud import storage


def delete_file_archived_generation(bucket_name, blob_name, generation):
    """Delete a blob in the bucket with the given generation."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # generation = 1579287380533984

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete_blob(blob_name, generation=generation)
    print(
        "Generation {} of blob {} was deleted from {}".format(
            generation, blob_name, bucket_name
        )
    )


# [END storage_delete_file_archived_generation]


if __name__ == "__main__":
    delete_file_archived_generation(
        bucket_name=sys.argv[1],
        blob_name=sys.argv[2],
        generation=sys.argv[3]
    )
