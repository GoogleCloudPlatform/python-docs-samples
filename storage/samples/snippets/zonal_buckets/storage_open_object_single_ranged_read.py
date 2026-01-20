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


# [START storage_open_object_single_ranged_read]
async def storage_open_object_single_ranged_read(
    bucket_name, object_name, start_byte, size, grpc_client=None
):
    """Downloads a range of bytes from an object.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    if grpc_client is None:
        grpc_client = AsyncGrpcClient().grpc_client

    mrd = AsyncMultiRangeDownloader(grpc_client, bucket_name, object_name)

    try:
        # Open the object, mrd always opens in read mode.
        await mrd.open()

        # requested range will be downloaded into this buffer, user may provide
        # their own buffer or file-like object.
        output_buffer = BytesIO()
        await mrd.download_ranges([(start_byte, size, output_buffer)])
    finally:
        if mrd.is_stream_open:
            await mrd.close()

    # Downloaded size can differ from requested size if object is smaller.
    # mrd will download at most up to the end of the object.
    downloaded_size = output_buffer.getbuffer().nbytes
    print(f"Downloaded {downloaded_size} bytes from {object_name}")


# [END storage_open_object_single_ranged_read]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")
    parser.add_argument(
        "--start_byte", type=int, help="The starting byte of the range."
    )
    parser.add_argument("--size", type=int, help="The number of bytes to download.")

    args = parser.parse_args()

    asyncio.run(
        storage_open_object_single_ranged_read(
            args.bucket_name, args.object_name, args.start_byte, args.size
        )
    )
