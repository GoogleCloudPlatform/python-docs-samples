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

# [START storage_control_disable_anywhere_cache]
from google.cloud import storage_control_v2


def disable_anywhere_cache(anywhere_cache_id: str) -> None:
    # The full name of the Anywhere Cache
    # anywhere_cache_id = "projects/_/buckets/bucket-name/anywhereCaches/zone-id"

    storage_control_client = storage_control_v2.StorageControlClient()

    request = storage_control_v2.DisableAnywhereCacheRequest(
        name=anywhere_cache_id,
    )
    # The DisableAnywhereCache RPC returns google.protobuf.Empty,
    # so we cannot access attributes like .name on the response.
    storage_control_client.disable_anywhere_cache(request=request)

    print(f"Disabled Anywhere Cache: {anywhere_cache_id}")


# [END storage_control_disable_anywhere_cache]


if __name__ == "__main__":
    disable_anywhere_cache(anywhere_cache_id=sys.argv[1])
