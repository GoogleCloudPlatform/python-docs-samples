#!/usr/bin/env python

# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

# [START storage_disable_ip_filtering]
from google.cloud import storage


def disable_ip_filtering(bucket_name):
    """Disables IP filtering on a bucket without deleting existing rules."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    if not bucket.ip_filter:
        print(f"No IP filter configuration found for bucket {bucket_name}.")
        return bucket

    ip_filter = bucket.ip_filter
    ip_filter.mode = "Disabled"
    # Re-assign to the bucket property to force google-cloud-storage to register
    # the nested changes for the patch() call.
    bucket.ip_filter = ip_filter
    bucket.patch()
    print(f"IP filtering disabled for bucket {bucket_name}.")
    return bucket


# [END storage_disable_ip_filtering]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python storage_disable_ip_filtering.py <bucket_name>")
        sys.exit(1)
    disable_ip_filtering(bucket_name=sys.argv[1])
