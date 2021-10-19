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

# [START storage_list_file_archived_generations]
from google.cloud import storage


def list_file_archived_generations(bucket_name):
    """Lists all the blobs in the bucket with generation."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    blobs = storage_client.list_blobs(bucket_name, versions=True)

    for blob in blobs:
        print("{},{}".format(blob.name, blob.generation))


# [END storage_list_file_archived_generations]


if __name__ == "__main__":
    list_file_archived_generations(bucket_name=sys.argv[1])
