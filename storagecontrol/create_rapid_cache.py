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

# [START storage_control_create_rapid_cache]
from google.cloud import storage_control_v2


def create_rapid_cache(bucket_name: str, zone: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The zone in which to create the Rapid Cache. The zone must be in the
    # same region as the bucket.
    # zone = "us-central1-a"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    project_path = storage_control_client.common_project_path("_")
    bucket_path = f"{project_path}/buckets/{bucket_name}"

    # Rapid Cache Ultra requires a bucket with hierarchical namespace enabled.
    rapid_cache = storage_control_v2.RapidCache(
        zone=zone,
        cache_type="rapid-cache-ultra",
    )
    request = storage_control_v2.CreateRapidCacheRequest(
        parent=bucket_path,
        rapid_cache=rapid_cache,
    )

    # Creating a Rapid Cache is a long-running operation.
    operation = storage_control_client.create_rapid_cache(request=request)
    response = operation.result()

    print(f"Created Rapid Cache: {response.name}")


# [END storage_control_create_rapid_cache]


if __name__ == "__main__":
    create_rapid_cache(bucket_name=sys.argv[1], zone=sys.argv[2])
