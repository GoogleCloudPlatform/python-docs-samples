#!/usr/bin/env python

# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

# [START storage_list_object_contexts]
from google.cloud import storage


def list_object_contexts(bucket_name, filter_string):
    """Lists objects in a bucket filtered by object contexts."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The filter to apply to the object contexts. Supported forms:
    #   contexts."KEY"="VALUE"   objects with the key set to the value
    #   contexts."KEY":*         objects that have the key
    #   -contexts."KEY":*        objects that don't have the key
    #   -contexts."KEY"="VALUE"  objects without the key set to the value
    # filter_string = 'contexts."key1"="value1"'

    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, filter_=filter_string)

    print(f"Objects matching filter {filter_string}:")
    for blob in blobs:
        print(blob.name)


# [END storage_list_object_contexts]

if __name__ == "__main__":
    list_object_contexts(bucket_name=sys.argv[1], filter_string=sys.argv[2])
