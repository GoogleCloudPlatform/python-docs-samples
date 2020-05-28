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

# [START storage_compose_file]
from google.cloud import storage


def compose_file(bucket_name, sources, destination_blob_name):
    """Concatenate source blobs into destination blob."""
    # bucket_name = "your-bucket-name"
    # sources = [blob_1, blob_2]
    # destination_blob_name = "destination-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination = bucket.blob(destination_blob_name)
    destination.content_type = "text/plain"
    destination.compose(sources)

    print(
        "Composed new object {} in the bucket {}".format(
            destination_blob_name, bucket.name
        )
    )
    return destination


# [END storage_compose_file]

if __name__ == "__main__":
    compose_file(
        bucket_name=sys.argv[1], sources=sys.argv[2], destination_blob_name=sys.argv[3],
    )
