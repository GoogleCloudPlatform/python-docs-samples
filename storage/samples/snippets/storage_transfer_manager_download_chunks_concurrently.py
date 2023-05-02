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


def download_chunks_concurrently(bucket_name, blob_name, filename, processes=8):
    """Download a single file in chunks, concurrently."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The file to be downloaded
    # blob_name = "target-file"

    # The destination filename or path
    # filename = ""

    # The maximum number of worker processes that should be used to handle the
    # workload of downloading the blob concurrently. PROCESS worker type uses more
    # system resources (both memory and CPU) and can result in faster operations
    # when working with large files. The optimal number of workers depends heavily
    # on the specific use case. Refer to the docstring of the underlining method
    # for more details.
    # processes=8

    from google.cloud.storage import Client, transfer_manager

    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    transfer_manager.download_chunks_concurrently(blob, filename, max_workers=processes)

    print("Downloaded {} to {}.".format(blob_name, filename))
