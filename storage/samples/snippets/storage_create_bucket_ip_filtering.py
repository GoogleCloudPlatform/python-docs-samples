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

# [START storage_create_bucket_ip_filtering]
from google.cloud import storage
from google.cloud.storage.ip_filter import IPFilter, PublicNetworkSource


def create_bucket_ip_filtering(bucket_name, public_cidr_range="192.0.2.0/24"):
    """Creates a new bucket with initial IP filtering rules pre-configured."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # public_cidr_range = "192.0.2.0/24"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    ip_filter = IPFilter()
    ip_filter.mode = "Disabled"
    ip_filter.public_network_source = PublicNetworkSource(
        allowed_ip_cidr_ranges=[public_cidr_range]
    )
    ip_filter.allow_all_service_agent_access = True

    bucket.ip_filter = ip_filter
    new_bucket = storage_client.create_bucket(bucket)

    print(
        f"Created bucket {new_bucket.name} with IP filtering mode: {new_bucket.ip_filter.mode}"
    )
    return new_bucket


# [END storage_create_bucket_ip_filtering]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python storage_create_bucket_ip_filtering.py <bucket_name> [public_cidr_range]"
        )
        sys.exit(1)
    if len(sys.argv) > 2:
        create_bucket_ip_filtering(
            bucket_name=sys.argv[1], public_cidr_range=sys.argv[2]
        )
    else:
        create_bucket_ip_filtering(bucket_name=sys.argv[1])
