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

from google.cloud.storage._experimental.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage._experimental.asyncio.async_grpc_client import AsyncGrpcClient


# [START storage_create_and_write_appendable_object]


async def storage_create_and_write_appendable_object(
    bucket_name, object_name, grpc_client=None
):
    """Uploads an appendable object to zonal bucket.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """

    if grpc_client is None:
        grpc_client = AsyncGrpcClient().grpc_client
    writer = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation=0,  # throws `FailedPrecondition` if object already exists.
    )
    # This creates a new appendable object of size 0 and opens it for appending.
    await writer.open()

    # appends data to the object
    # you can perform `.append` multiple times as needed. Data will be appended
    # to the end of the object.
    await writer.append(b"Some data")

    # Once all appends are done, close the gRPC bidirectional stream.
    await writer.close()

    print(
        f"Appended object {object_name} created of size {writer.persisted_size} bytes."
    )


# [END storage_create_and_write_appendable_object]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")

    args = parser.parse_args()

    asyncio.run(
        storage_create_and_write_appendable_object(
            bucket_name=args.bucket_name,
            object_name=args.object_name,
        )
    )
