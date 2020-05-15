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

import base64
import sys

# [START storage_object_csek_to_cmek]
from google.cloud import storage


def object_csek_to_cmek(bucket_name, blob_name, encryption_key, kms_key_name):
    """Change a blob's customer-supplied encryption key to KMS key"""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # encryption_key = "TIbv/fjexq+VmtXzAlc63J4z5kFmWJ6NdAPQulQBT7g="
    # kms_key_name = "projects/PROJ/locations/LOC/keyRings/RING/cryptoKey/KEY"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    current_encryption_key = base64.b64decode(encryption_key)
    source_blob = bucket.blob(blob_name, encryption_key=current_encryption_key)

    destination_blob = bucket.blob(blob_name, kms_key_name=kms_key_name)
    token, rewritten, total = destination_blob.rewrite(source_blob)

    while token is not None:
        token, rewritten, total = destination_blob.rewrite(source_blob, token=token)

    print(
        "Blob {} in bucket {} is now managed by the KMS key {} instead of a customer-supplied encryption key".format(
            blob_name, bucket_name, kms_key_name
        )
    )
    return destination_blob


# [END storage_object_csek_to_cmek]

if __name__ == "__main__":
    object_csek_to_cmek(
        bucket_name=sys.argv[1],
        blob_name=sys.argv[2],
        encryption_key=sys.argv[3],
        kms_key_name=sys.argv[4],
    )
