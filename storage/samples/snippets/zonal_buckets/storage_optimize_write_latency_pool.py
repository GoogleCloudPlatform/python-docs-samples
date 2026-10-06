#!/usr/bin/env python

# Copyright 2026 Google LLC
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
from collections import deque
from io import BytesIO

from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)


# [START storage_optimize_write_latency_pool]
async def storage_optimize_write_latency_pool(
    bucket_name: str, key_prefix: str, pool_size: int = 3, grpc_client=None
):
    """Uses a pre-warmed pool of writers for a zonal bucket.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    # The ID of your GCS zonal bucket
    # bucket_name = "your-unique-bucket-name"

    # The prefix for your pooled GCS objects
    # key_prefix = "pooled-object"

    grpc_client_created = False
    if grpc_client is None:
        grpc_client = AsyncGrpcClient()
        grpc_client_created = True

    next_object_name = f"{key_prefix}_{pool_size}"

    async def new_prewarmed_writer(name: str) -> AsyncAppendableObjectWriter:
        w = AsyncAppendableObjectWriter(
            client=grpc_client,
            bucket_name=bucket_name,
            object_name=name,
            generation=0,
        )
        await w.open()  # Establishes stream and creates 0-byte object in background.
        return w

    # 1. Init pool: Sized to ensure pre-warmed writers are always available.
    pool = deque(
        await asyncio.gather(
            *(
                new_prewarmed_writer(f"{key_prefix}_{i}")
                for i in range(pool_size)
            )
        )
    )

    try:
        # 2. Write: Pop a pre-warmed writer; append() writes and flushes data
        # (~1-2 ms).
        writer = pool.popleft()
        await writer.append(b"0123456789")

        # 3. Pool maintenance (run asynchronously off the critical write path):
        # Close the used writer without finalizing and refill the pool.
        async def maintain_pool(
            used: AsyncAppendableObjectWriter, next_name: str
        ):
            await used.close(finalize_on_close=False)
            pool.append(await new_prewarmed_writer(next_name))

        maintenance_task = asyncio.create_task(
            maintain_pool(writer, next_object_name)
        )

        # 4. Read: Unfinalized objects are readable after flush().
        mrd = AsyncMultiRangeDownloader(
            grpc_client, bucket_name, f"{key_prefix}_0"
        )
        await mrd.open()
        buf = BytesIO()
        await mrd.download_ranges([(0, 0, buf)])
        await mrd.close()

        await maintenance_task
        print(
            f"Read unfinalized object {key_prefix}_0: "
            f"{buf.getvalue().decode('utf-8')}"
        )
    finally:
        for rem in pool:
            await rem.close(finalize_on_close=False)
        if grpc_client_created:
            await grpc_client.close()


# [END storage_optimize_write_latency_pool]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--bucket_name", help="Your Cloud Storage zonal bucket name."
    )
    parser.add_argument(
        "--key_prefix", help="Prefix for pooled object names."
    )
    args = parser.parse_args()

    asyncio.run(
        storage_optimize_write_latency_pool(
            bucket_name=args.bucket_name,
            key_prefix=args.key_prefix,
        )
    )
