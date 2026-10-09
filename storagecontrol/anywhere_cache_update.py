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
from google.protobuf import field_mask_pb2


def update_anywhere_cache(anywhere_cache_id: str, admission_policy: str) -> None:
    # The full name of the Anywhere Cache
    # anywhere_cache_id = "projects/_/buckets/bucket-name/anywhereCaches/zone-id"

    # The new admission policy
    # admission_policy = "admit-on-second-miss"

    storage_control_client = storage_control_v2.StorageControlClient()

    anywhere_cache = storage_control_v2.AnywhereCache(
        name=anywhere_cache_id,
        admission_policy=admission_policy,
    )
    update_mask = field_mask_pb2.FieldMask(paths=["admission_policy"])

    request = storage_control_v2.UpdateAnywhereCacheRequest(
        anywhere_cache=anywhere_cache,
        update_mask=update_mask,
    )
    # This operation is long-running. Real-world applications may want to
    # use callbacks, coroutines, or polling to handle the response.
    operation = storage_control_client.update_anywhere_cache(request=request)
    response = operation.result()

    print(f"Updated Anywhere Cache: {response.name}")
    print(f"New Admission Policy: {response.admission_policy}")


# [END storage_control_update_anywhere_cache]


if __name__ == "__main__":
    update_anywhere_cache(anywhere_cache_id=sys.argv[1], admission_policy=sys.argv[2])
