#!/usr/bin/env python

# Copyright 2025 Google LLC
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

import sys

# [START storage_disable_soft_delete]
from google.cloud import storage


def disable_soft_delete(bucket_name):
    """Disable soft-delete policy for the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Setting the retention duration to 0 disables soft-delete.
    bucket.soft_delete_policy.retention_duration_seconds = 0
    bucket.patch()

    print(f"Soft-delete policy is disabled for bucket {bucket_name}")


# [END storage_disable_soft_delete]

if __name__ == "__main__":
    disable_soft_delete(bucket_name=sys.argv[1])
