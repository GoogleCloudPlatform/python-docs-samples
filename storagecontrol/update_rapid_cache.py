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

# [START storage_control_update_rapid_cache]
from google.cloud import storage_control_v2
from google.protobuf import duration_pb2
from google.protobuf import field_mask_pb2


def update_rapid_cache(bucket_name: str, cache_id: str, ttl_seconds: int) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The ID of the Rapid Cache, which is the same as its zone
    # cache_id = "us-central1-a"

    # The new time to live (TTL) for cache entries, in seconds. The TTL must
    # be between 1 hour and 7 days.
    # ttl_seconds = 172800  # 2 days

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    rapid_cache_path = storage_control_client.rapid_cache_path(
        project="_", bucket=bucket_name, rapid_cache=cache_id
    )

    rapid_cache = storage_control_v2.RapidCache(
        name=rapid_cache_path,
        ttl=duration_pb2.Duration(seconds=ttl_seconds),
    )
    # Only the fields listed in the update mask are changed.
    update_mask = field_mask_pb2.FieldMask(paths=["ttl"])
    request = storage_control_v2.UpdateRapidCacheRequest(
        rapid_cache=rapid_cache,
        update_mask=update_mask,
    )

    # Updating a Rapid Cache is a long-running operation.
    operation = storage_control_client.update_rapid_cache(request=request)
    response = operation.result()

    print(f"Updated Rapid Cache: {response.name}")
    # The client library returns the TTL as a datetime.timedelta.
    print(f"TTL: {response.ttl.total_seconds():.0f} seconds")


# [END storage_control_update_rapid_cache]


if __name__ == "__main__":
    update_rapid_cache(
        bucket_name=sys.argv[1],
        cache_id=sys.argv[2],
        ttl_seconds=int(sys.argv[3]),
    )
