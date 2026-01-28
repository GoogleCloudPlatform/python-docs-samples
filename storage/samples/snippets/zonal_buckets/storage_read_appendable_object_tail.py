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
import time
from datetime import datetime
from io import BytesIO

from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage._experimental.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)

BYTES_TO_APPEND = b"fav_bytes."
NUM_BYTES_TO_APPEND_EVERY_SECOND = len(BYTES_TO_APPEND)


# [START storage_read_appendable_object_tail]
async def appender(writer: AsyncAppendableObjectWriter, duration: int):
    """Appends 10 bytes to the object every second for a given duration."""
    print("Appender started.")
    bytes_appended = 0
    for i in range(duration):
        await writer.append(BYTES_TO_APPEND)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        bytes_appended += NUM_BYTES_TO_APPEND_EVERY_SECOND
        print(
            f"[{now}] Appended {NUM_BYTES_TO_APPEND_EVERY_SECOND} new bytes. Total appended: {bytes_appended} bytes."
        )
        await asyncio.sleep(1)
    print("Appender finished.")


async def tailer(
    bucket_name: str, object_name: str, duration: int, client: AsyncGrpcClient
):
    """Tails the object by reading new data as it is appended."""
    print("Tailer started.")
    start_byte = 0
    start_time = time.monotonic()
    mrd = AsyncMultiRangeDownloader(client, bucket_name, object_name)
    try:
        await mrd.open()
        # Run the tailer for the specified duration.
        while time.monotonic() - start_time < duration:
            output_buffer = BytesIO()
            # A download range of (start, 0) means to read from 'start' to the end.
            await mrd.download_ranges([(start_byte, 0, output_buffer)])

            bytes_downloaded = output_buffer.getbuffer().nbytes
            if bytes_downloaded > 0:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print(
                    f"[{now}] Tailer read {bytes_downloaded} new bytes: {output_buffer.getvalue()}"
                )
                start_byte += bytes_downloaded

            await asyncio.sleep(0.1)  # Poll for new data every 0.1 seconds.
    finally:
        if mrd.is_stream_open:
            await mrd.close()
    print("Tailer finished.")


# read_appendable_object_tail simulates a "tail -f" command on a GCS object. It
# repeatedly polls an appendable object for new content. In a real
# application, the object would be written to by a separate process.
async def read_appendable_object_tail(
    bucket_name: str, object_name: str, duration: int, grpc_client=None
):
    """Main function to create an appendable object and run tasks.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    if grpc_client is None:
        grpc_client = AsyncGrpcClient()
    writer = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
    )
    # 1. Create an empty appendable object.
    try:
        # 1. Create an empty appendable object.
        await writer.open()
        print(f"Created empty appendable object: {object_name}")

        # 2. Create the appender and tailer coroutines.
        appender_task = asyncio.create_task(appender(writer, duration))
        tailer_task = asyncio.create_task(
            tailer(bucket_name, object_name, duration, grpc_client)
        )

        # 3. Execute the coroutines concurrently.
        await asyncio.gather(appender_task, tailer_task)
    finally:
        if writer._is_stream_open:
            await writer.close()
            print("Writer closed.")


# [END storage_read_appendable_object_tail]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Demonstrates tailing an appendable GCS object.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument(
        "--object_name", help="Your Cloud Storage object name to be created."
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration in seconds to run the demo.",
    )

    args = parser.parse_args()

    asyncio.run(
        read_appendable_object_tail(args.bucket_name, args.object_name, args.duration)
    )
