#!/usr/bin/env python

# Copyright 2022 Google LLC
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

# [START storage_stream_file_download]
from google.cloud import storage


def download_blob_to_stream(bucket_name, source_blob_name, file_obj):
    """Downloads a blob to a stream or other file-like object."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object (blob)
    # source_blob_name = "storage-object-name"

    # The stream or file (file-like object) to which the blob will be written
    # import io
    # file_obj = io.BytesIO()

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client-side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` in that it doesn't
    # retrieve metadata from Google Cloud Storage. As we don't use metadata in
    # this example, using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_file(file_obj)

    print(f"Downloaded blob {source_blob_name} to file-like object.")

    return file_obj
    # Before reading from file_obj, remember to rewind with file_obj.seek(0).

# [END storage_stream_file_download]
