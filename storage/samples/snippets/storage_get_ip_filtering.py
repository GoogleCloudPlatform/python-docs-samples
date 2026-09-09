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
from google.cloud import storage


def get_ip_filtering(bucket_name):
    """Retrieves and prints the IP filtering configuration of a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    ip_filter = bucket.ip_filter
    if not ip_filter:
        print(f"Bucket {bucket_name} has no IP Filter configured.")
        return None

    print(f"IP Filter Configuration for {bucket_name}:")
    print(f"Mode: {ip_filter.mode}")
    print(f"Allow All Service Agent Access: {ip_filter.allow_all_service_agent_access}")
    print(f"Allow Cross Org VPCs: {ip_filter.allow_cross_org_vpcs}")

    if ip_filter.public_network_source:
        print(
            f"Public CIDR Ranges: {ip_filter.public_network_source.allowed_ip_cidr_ranges}"
        )

    if ip_filter.vpc_network_sources:
        for vpc in ip_filter.vpc_network_sources:
            print(
                f"VPC Network: {vpc.network}, CIDR Ranges: {vpc.allowed_ip_cidr_ranges}"
            )

    return ip_filter


# [END storage_get_ip_filtering]

if __name__ == "__main__":
    get_ip_filtering(bucket_name=sys.argv[1])
