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


# [START storage_upload_encrypted_file]
import base64
# [END storage_upload_encrypted_file]
import sys
# [START storage_upload_encrypted_file]

from google.cloud import storage


def upload_encrypted_blob(
    bucket_name,
    source_file_name,
    destination_blob_name,
    base64_encryption_key,
):
    """Uploads a file to a Google Cloud Storage bucket using a custom
    encryption key.

    The file will be encrypted by Google Cloud Storage and only
    retrievable using the provided encryption key.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Encryption key must be an AES256 key represented as a bytestring with
    # 32 bytes. Since it's passed in as a base64 encoded string, it needs
    # to be decoded.
    encryption_key = base64.b64decode(base64_encryption_key)
    blob = bucket.blob(
        destination_blob_name, encryption_key=encryption_key
    )

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


# [END storage_upload_encrypted_file]

if __name__ == "__main__":
    upload_encrypted_blob(
        bucket_name=sys.argv[1],
        source_file_name=sys.argv[2],
        destination_blob_name=sys.argv[3],
        base64_encryption_key=sys.argv[4],
    )
