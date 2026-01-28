#!/usr/bin/env python

# Copyright 2026 Google Inc. All Rights Reserved.
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

import argparse
import asyncio
from io import BytesIO

from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)


# [START storage_open_object_read_full_object]
async def storage_open_object_read_full_object(
    bucket_name, object_name, grpc_client=None
):
    """Downloads the entire content of an object using a multi-range downloader.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    if grpc_client is None:
        grpc_client = AsyncGrpcClient()

    # mrd = Multi-Range-Downloader
    mrd = AsyncMultiRangeDownloader(grpc_client, bucket_name, object_name)

    try:
        # Open the object, mrd always opens in read mode.
        await mrd.open()

        # This could be any buffer or file-like object.
        output_buffer = BytesIO()
        # A download range of (0, 0) means to read from the beginning to the end.
        await mrd.download_ranges([(0, 0, output_buffer)])
    finally:
        if mrd.is_stream_open:
            await mrd.close()

    downloaded_bytes = output_buffer.getvalue()
    print(
        f"Downloaded all {len(downloaded_bytes)} bytes from object {object_name} in bucket {bucket_name}."
    )


# [END storage_open_object_read_full_object]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")

    args = parser.parse_args()

    asyncio.run(
        storage_open_object_read_full_object(args.bucket_name, args.object_name)
    )
