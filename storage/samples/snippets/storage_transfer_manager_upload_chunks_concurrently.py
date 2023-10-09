# Copyright 2023 Google LLC
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

# [START storage_transfer_manager_upload_chunks_concurrently]
def upload_chunks_concurrently(
    bucket_name,
    source_filename,
    destination_blob_name,
    chunk_size=32 * 1024 * 1024,
    workers=8,
):
    """Upload a single file, in chunks, concurrently in a process pool."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The path to your file to upload
    # source_filename = "local/path/to/file"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # The size of each chunk. The performance impact of this value depends on
    # the use case. The remote service has a minimum of 5 MiB and a maximum of
    # 5 GiB.
    # chunk_size = 32 * 1024 * 1024 (32 MiB)

    # The maximum number of processes to use for the operation. The performance
    # impact of this value depends on the use case. Each additional process
    # occupies some CPU and memory resources until finished. Threads can be used
    # instead of processes by passing `worker_type=transfer_manager.THREAD`.
    # workers=8

    from google.cloud.storage import Client, transfer_manager

    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    transfer_manager.upload_chunks_concurrently(
        source_filename, blob, chunk_size=chunk_size, max_workers=workers
    )

    print(f"File {source_filename} uploaded to {destination_blob_name}.")


# [END storage_transfer_manager_upload_chunks_concurrently]
