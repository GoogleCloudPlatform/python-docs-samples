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


# [START storage_finalize_appendable_object_upload]
async def storage_finalize_appendable_object_upload(
    bucket_name, object_name, grpc_client=None
):
    """Creates, writes to, and finalizes an appendable object.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """

    if grpc_client is None:
        grpc_client = AsyncGrpcClient()
    writer = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation=0,  # throws `FailedPrecondition` if object already exists.
    )
    # This creates a new appendable object of size 0 and opens it for appending.
    await writer.open()

    # Appends data to the object.
    await writer.append(b"Some data")

    # finalize the appendable object,
    # NOTE:
    # 1. once finalized no more appends can be done to the object.
    # 2. If you don't want to finalize, you can simply call `writer.close`
    # 3. calling `.finalize()` also closes the grpc-bidi stream, calling
    #   `.close` after `.finalize` may lead to undefined behavior.
    object_resource = await writer.finalize()

    print(f"Appendable object {object_name} created and finalized.")
    print("Object Metadata:")
    print(object_resource)


# [END storage_finalize_appendable_object_upload]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")

    args = parser.parse_args()

    asyncio.run(
        storage_finalize_appendable_object_upload(
            bucket_name=args.bucket_name,
            object_name=args.object_name,
        )
    )
