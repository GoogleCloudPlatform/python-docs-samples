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

from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient


# [START storage_pause_and_resume_appendable_upload]
async def storage_pause_and_resume_appendable_upload(
    bucket_name, object_name, grpc_client=None
):
    """Demonstrates pausing and resuming an appendable object upload.

    grpc_client: an existing grpc_client to use, this is only for testing.
    """
    if grpc_client is None:
        grpc_client = AsyncGrpcClient()

    writer1 = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
    )
    await writer1.open()
    await writer1.append(b"First part of the data. ")
    print(f"Appended {writer1.persisted_size} bytes with the first writer.")

    # 2. After appending some data, close the writer to "pause" the upload.
    #  NOTE: you can pause indefinitely and still read the conetent uploaded so far using MRD.
    await writer1.close()

    print("First writer closed. Upload is 'paused'.")

    # 3. Create a new writer, passing the generation number from the previous
    #    writer. This is a precondition to ensure that the object hasn't been
    #    modified since we last accessed it.
    generation_to_resume = writer1.generation
    print(f"Generation to resume from is: {generation_to_resume}")

    writer2 = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation=generation_to_resume,
    )
    # 4. Open the new writer.
    try:
        await writer2.open()

        # 5. Append some more data using the new writer.
        await writer2.append(b"Second part of the data.")
        print(f"Appended more data. Total size is now {writer2.persisted_size} bytes.")
    finally:
        # 6. Finally, close the new writer.
        if writer2._is_stream_open:
            await writer2.close()
    print("Second writer closed. Full object uploaded.")


# [END storage_pause_and_resume_appendable_upload]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bucket_name", help="Your Cloud Storage bucket name.")
    parser.add_argument("--object_name", help="Your Cloud Storage object name.")

    args = parser.parse_args()

    asyncio.run(
        storage_pause_and_resume_appendable_upload(
            bucket_name=args.bucket_name,
            object_name=args.object_name,
        )
    )
