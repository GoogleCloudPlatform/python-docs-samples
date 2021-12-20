#!/usr/bin/env python

# Copyright 2021 Google LLC
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

# [START storage_download_byte_range]
from google.cloud import storage


def download_byte_range(
    bucket_name, source_blob_name, start_byte, end_byte, destination_file_name
):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The starting byte at which to begin the download
    # start_byte = 0

    # The ending byte at which to end the download
    # end_byte = 20

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name, start=start_byte, end=end_byte)

    print(
        "Downloaded bytes {} to {} of object {} from bucket {} to local file {}.".format(
            start_byte, end_byte, source_blob_name, bucket_name, destination_file_name
        )
    )


# [END storage_download_byte_range]

if __name__ == "__main__":
    download_byte_range(
        bucket_name=sys.argv[1],
        source_blob_name=sys.argv[2],
        start_byte=sys.argv[3],
        end_byte=sys.argv[4],
        destination_file_name=sys.argv[5],
    )
