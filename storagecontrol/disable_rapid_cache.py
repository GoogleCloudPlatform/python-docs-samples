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

# [START storage_control_disable_rapid_cache]
from google.cloud import storage_control_v2


def disable_rapid_cache(bucket_name: str, cache_id: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    # The ID of the Rapid Cache
    # cache_id = "your-rapid-cache-id"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage bucket path uses the global access pattern, in which the "_"
    # denotes this bucket exists in the global namespace.
    rapid_cache_path = storage_control_client.rapid_cache_path(
        project="_", bucket=bucket_name, rapid_cache=cache_id
    )

    request = storage_control_v2.DisableRapidCacheRequest(name=rapid_cache_path)

    # Disabling a Rapid Cache starts a long-running operation. The cache moves
    # to the "disabled" state within seconds, but the operation only completes
    # once the cache has been fully removed, which can take more than 30
    # minutes. This sample does not wait for the operation to complete; use
    # get_rapid_cache to check the cache state.
    operation = storage_control_client.disable_rapid_cache(request=request)

    print(f"Disabling Rapid Cache: {rapid_cache_path}")
    print(f"Operation: {operation.operation.name}")


# [END storage_control_disable_rapid_cache]


if __name__ == "__main__":
    disable_rapid_cache(bucket_name=sys.argv[1], cache_id=sys.argv[2])
