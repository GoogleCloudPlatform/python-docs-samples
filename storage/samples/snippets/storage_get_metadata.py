#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
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

# [START storage_get_metadata]
from google.cloud import storage


def blob_metadata(bucket_name, blob_name):
    """Prints out a blob's metadata."""
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Retrieve a blob, and its metadata, from Google Cloud Storage.
    # Note that `get_blob` differs from `Bucket.blob`, which does not
    # make an HTTP request.
    blob = bucket.get_blob(blob_name)

    print(f"Blob: {blob.name}")
    print(f"Blob finalization: {blob.finalized_time}")
    print(f"Bucket: {blob.bucket.name}")
    print(f"Storage class: {blob.storage_class}")
    print(f"ID: {blob.id}")
    print(f"Size: {blob.size} bytes")
    print(f"Updated: {blob.updated}")
    print(f"Generation: {blob.generation}")
    print(f"Metageneration: {blob.metageneration}")
    print(f"Etag: {blob.etag}")
    print(f"Owner: {blob.owner}")
    print(f"Component count: {blob.component_count}")
    print(f"Crc32c: {blob.crc32c}")
    print(f"md5_hash: {blob.md5_hash}")
    print(f"Cache-control: {blob.cache_control}")
    print(f"Content-type: {blob.content_type}")
    print(f"Content-disposition: {blob.content_disposition}")
    print(f"Content-encoding: {blob.content_encoding}")
    print(f"Content-language: {blob.content_language}")
    print(f"Metadata: {blob.metadata}")
    print(f"Medialink: {blob.media_link}")
    print(f"Custom Time: {blob.custom_time}")
    print("Temporary hold: ", "enabled" if blob.temporary_hold else "disabled")
    print(
        "Event based hold: ",
        "enabled" if blob.event_based_hold else "disabled",
    )
    print(f"Retention mode: {blob.retention.mode}")
    print(f"Retention retain until time: {blob.retention.retain_until_time}")
    if blob.retention_expiration_time:
        print(
            f"retentionExpirationTime: {blob.retention_expiration_time}"
        )


# [END storage_get_metadata]

if __name__ == "__main__":
    blob_metadata(bucket_name=sys.argv[1], blob_name=sys.argv[2])
