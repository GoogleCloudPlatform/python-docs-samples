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

# [START storage_get_ip_filtering]
from typing import Optional

from google.cloud import storage
from google.cloud.storage.ip_filter import IPFilter


def get_ip_filtering(bucket_name: str) -> Optional[IPFilter]:
    """Retrieves and prints the IP filtering configuration of a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    ip_filter = bucket.ip_filter
    if not ip_filter:
        print(f"Bucket {bucket_name} has no IP Filter configured.")
        return None

    print(f"IP Filter mode: {ip_filter.mode}")
    print(f"IP Filter configuration: {ip_filter._to_api_resource()}")

    return ip_filter


# [END storage_get_ip_filtering]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python storage_get_ip_filtering.py <bucket_name>")
        sys.exit(1)
    get_ip_filtering(bucket_name=sys.argv[1])
