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

# [START storage_get_soft_delete_policy]
from google.cloud import storage


def get_soft_delete_policy(bucket_name):
    """Gets the soft-delete policy of the bucket"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    print(f"Soft-delete policy for {bucket_name}")
    if (
        bucket.soft_delete_policy
        and bucket.soft_delete_policy.retention_duration_seconds
    ):
        print("Object soft-delete policy is enabled")
        print(
            f"Object retention duration: {bucket.soft_delete_policy.retention_duration_seconds} seconds"
        )
        print(f"Policy effective time: {bucket.soft_delete_policy.effective_time}")
    else:
        print("Object soft-delete policy is disabled")


# [END storage_get_soft_delete_policy]

if __name__ == "__main__":
    get_soft_delete_policy(bucket_name=sys.argv[1])
