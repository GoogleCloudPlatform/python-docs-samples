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


# [START storage_open_object_multiple_ranged_read]
async def storage_open_object_multiple_ranged_read(
    bucket_name, object_name, grpc_client=None
):
    """Downloads multiple ranges of bytes from a single object into different buffers.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    if grpc_client is None:
        grpc_client = AsyncGrpcClient()

    mrd = AsyncMultiRangeDownloader(grpc_client, bucket_name, object_name)

    try:
        # Open the object, mrd always opens in read mode.
        await mrd.open()

        # Specify four different buffers to download ranges into.
        buffers = [BytesIO(), BytesIO(), BytesIO(), BytesIO()]

        # Define the ranges to download. Each range is a tuple of (start_byte, size, buffer).
        # All ranges will download 10 bytes from different starting positions.
        # We choose arbitrary start bytes for this example. An object should be large enough.
        # A user can choose any start byte between 0 and `object_size`.
        # If `start_bytes` is greater than `object_size`, mrd will throw an error.
        ranges = [
            (0, 10, buffers[0]),
            (20, 10, buffers[1]),
            (40, 10, buffers[2]),
            (60, 10, buffers[3]),
        ]

        await mrd.download_ranges(ranges)

    finally:
        await mrd.close()

    # Print the downloaded content from each buffer.
    for i, output_buffer in enumerate(buffers):
        downloaded_size = output_buffer.getbuffer().nbytes
        print(
            f"Downloaded {downloaded_size} bytes into buffer {i + 1} from start byte {ranges[i][0]}: {output_buffer.getvalue()}"
        )


# [END storage_open_object_multiple_ranged_read]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")

    args = parser.parse_args()

    asyncio.run(
        storage_open_object_multiple_ranged_read(args.bucket_name, args.object_name)
    )
