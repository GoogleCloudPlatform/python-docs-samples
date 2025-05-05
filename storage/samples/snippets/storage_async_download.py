#!/usr/bin/env python

# Copyright 2025 Google LLC.
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

import asyncio
import argparse

"""Sample that asynchronously downloads multiple files from GCS to application's memory.
"""


# [START storage_async_download]
# This sample can be run by calling `async.run(async_download_blobs('bucket_name', ['file1', 'file2']))`
async def async_download_blobs(bucket_name, *file_names):
    """Downloads a number of files in parallel from the bucket.
    """
    # The ID of your GCS bucket.
    # bucket_name = "your-bucket-name"

    # The list of files names to download, these files should be present in bucket.
    # file_names = ["myfile1", "myfile2"]

    import asyncio
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    loop = asyncio.get_running_loop()

    tasks = []
    for file_name in file_names:
        blob = bucket.blob(file_name)
        # The first arg, None, tells it to use the default loops executor
        tasks.append(loop.run_in_executor(None, blob.download_as_bytes))

    # If the method returns a value (such as download_as_bytes), gather will return the values
    _ = await asyncio.gather(*tasks)
    for file_name in file_names:
        print(f"Downloaded storage object {file_name}")


# [END storage_async_download]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket_name', type=str, dest='bucket_name', help='provide the name of the GCS bucket')
    parser.add_argument(
        '-f', '--file_name',
        action='append',
        type=str,
        dest='file_names',
        help='Example: -f file1.txt or --file_name my_fav.mp4 . It can be used multiple times.'
    )
    args = parser.parse_args()

    asyncio.run(async_download_blobs(args.bucket_name, *args.file_names))
