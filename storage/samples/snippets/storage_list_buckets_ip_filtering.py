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

# [START storage_list_buckets_ip_filtering]
from typing import List

from google.cloud import storage


def list_buckets_ip_filtering() -> List[storage.Bucket]:
    """Lists all buckets in the project with their IP filtering status."""
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())

    for bucket in buckets:
        status = (
            bucket.ip_filter.mode
            if bucket.ip_filter and bucket.ip_filter.mode
            else "Not Configured"
        )
        print(f"Bucket: {bucket.name}, IP Filter Mode: {status}")

    return buckets


# [END storage_list_buckets_ip_filtering]

if __name__ == "__main__":
    list_buckets_ip_filtering()
