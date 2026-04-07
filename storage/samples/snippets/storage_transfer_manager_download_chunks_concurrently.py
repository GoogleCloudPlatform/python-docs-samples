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

# [START storage_transfer_manager_download_chunks_concurrently]
def download_chunks_concurrently(
    bucket_name, blob_name, filename, chunk_size=32 * 1024 * 1024, workers=8
):
    """Download a single file in chunks, concurrently in a process pool."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The file to be downloaded
    # blob_name = "target-file"

    # The destination filename or path
    # filename = ""

    # The size of each chunk. The performance impact of this value depends on
    # the use case. The remote service has a minimum of 5 MiB and a maximum of
    # 5 GiB.
    # chunk_size = 32 * 1024 * 1024 (32 MiB)

    # The maximum number of processes to use for the operation. The performance
    # impact of this value depends on the use case, but smaller files usually
    # benefit from a higher number of processes. Each additional process occupies
    # some CPU and memory resources until finished. Threads can be used instead
    # of processes by passing `worker_type=transfer_manager.THREAD`.
    # workers=8

    from google.cloud.storage import Client, transfer_manager

    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    transfer_manager.download_chunks_concurrently(
        blob, filename, chunk_size=chunk_size, max_workers=workers
    )

    print("Downloaded {} to {}.".format(blob_name, filename))


# [END storage_transfer_manager_download_chunks_concurrently]
