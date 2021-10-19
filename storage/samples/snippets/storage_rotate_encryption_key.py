#!/usr/bin/env python

# Copyright 2019 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START storage_rotate_encryption_key]
import base64
# [END storage_rotate_encryption_key]
import sys
# [START storage_rotate_encryption_key]

from google.cloud import storage


def rotate_encryption_key(
    bucket_name, blob_name, base64_encryption_key, base64_new_encryption_key
):
    """Performs a key rotation by re-writing an encrypted blob with a new
    encryption key."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    current_encryption_key = base64.b64decode(base64_encryption_key)
    new_encryption_key = base64.b64decode(base64_new_encryption_key)

    # Both source_blob and destination_blob refer to the same storage object,
    # but destination_blob has the new encryption key.
    source_blob = bucket.blob(
        blob_name, encryption_key=current_encryption_key
    )
    destination_blob = bucket.blob(
        blob_name, encryption_key=new_encryption_key
    )

    token = None

    while True:
        token, bytes_rewritten, total_bytes = destination_blob.rewrite(
            source_blob, token=token
        )
        if token is None:
            break

    print("Key rotation complete for Blob {}".format(blob_name))


# [END storage_rotate_encryption_key]

if __name__ == "__main__":
    rotate_encryption_key(
        bucket_name=sys.argv[1],
        blob_name=sys.argv[2],
        base64_encryption_key=sys.argv[3],
        base64_new_encryption_key=sys.argv[4],
    )
