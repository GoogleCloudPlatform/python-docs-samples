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

# [START storage_download_encrypted_file]
import base64
# [END storage_download_encrypted_file]
import sys
# [START storage_download_encrypted_file]

from google.cloud import storage


def download_encrypted_blob(
    bucket_name,
    source_blob_name,
    destination_file_name,
    base64_encryption_key,
):
    """Downloads a previously-encrypted blob from Google Cloud Storage.

    The encryption key provided must be the same key provided when uploading
    the blob.
    """
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"
    # base64_encryption_key = "base64-encoded-encryption-key"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Encryption key must be an AES256 key represented as a bytestring with
    # 32 bytes. Since it's passed in as a base64 encoded string, it needs
    # to be decoded.
    encryption_key = base64.b64decode(base64_encryption_key)
    blob = bucket.blob(source_blob_name, encryption_key=encryption_key)

    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


# [END storage_download_encrypted_file]

if __name__ == "__main__":
    download_encrypted_blob(
        bucket_name=sys.argv[1],
        source_blob_name=sys.argv[2],
        destination_file_name=sys.argv[3],
        base64_encryption_key=sys.argv[4],
    )
