# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_control_update_anywhere_cache]
from google.cloud import storage_control_v2
from google.protobuf import duration_pb2
from google.protobuf import field_mask_pb2


def update_anywhere_cache(bucket_name: str, zone: str, ttl_seconds: int) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The zone where the cache was created
    # zone = "us-central1-f"

    # The new TTL in seconds
    # ttl_seconds = 86400

    storage_control_client = storage_control_v2.StorageControlClient()

    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = storage_control_client.common_project_path("_")
    cache_path = f"{project_path}/buckets/{bucket_name}/anywhereCaches/{zone}"

    anywhere_cache = storage_control_v2.AnywhereCache(
        name=cache_path,
        ttl=duration_pb2.Duration(seconds=ttl_seconds),
    )

    update_mask = field_mask_pb2.FieldMask(paths=["ttl"])

    request = storage_control_v2.UpdateAnywhereCacheRequest(
        anywhere_cache=anywhere_cache,
        update_mask=update_mask,
    )

    operation = storage_control_client.update_anywhere_cache(request=request)

    print("Waiting for operation to complete...")
    response = operation.result()

    print(f"Updated anywhere cache: {response.name}")


# [END storage_control_update_anywhere_cache]


if __name__ == "__main__":
    update_anywhere_cache(
        bucket_name=sys.argv[1], zone=sys.argv[2], ttl_seconds=int(sys.argv[3])
    )
