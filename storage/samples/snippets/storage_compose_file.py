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


def compose_file(bucket_name, first_blob_name, second_blob_name, destination_blob_name):
    """Concatenate source blobs into destination blob."""
    # bucket_name = "your-bucket-name"
    # first_blob_name = "first-object-name"
    # second_blob_name = "second-blob-name"
    # destination_blob_name = "destination-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination = bucket.blob(destination_blob_name)
    destination.content_type = "text/plain"

    # Note sources is a list of Blob instances, up to the max of 32 instances per request
    sources = [bucket.blob(first_blob_name), bucket.blob(second_blob_name)]

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to compose is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    # There is also an `if_source_generation_match` parameter, which is not used in this example.
    destination_generation_match_precondition = 0

    destination.compose(sources, if_generation_match=destination_generation_match_precondition)

    print(
        "New composite object {} in the bucket {} was created by combining {} and {}".format(
            destination_blob_name, bucket_name, first_blob_name, second_blob_name
        )
    )
    return destination


# [END storage_compose_file]

if __name__ == "__main__":
    compose_file(
        bucket_name=sys.argv[1],
        first_blob_name=sys.argv[2],
        second_blob_name=sys.argv[3],
        destination_blob_name=sys.argv[4],
    )
