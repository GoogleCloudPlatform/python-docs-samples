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

# [START storage_enable_ip_filtering]
from google.cloud import storage
from google.cloud.storage.ip_filter import (
    IPFilter,
    PublicNetworkSource,
    VpcNetworkSource,
)


def enable_ip_filtering(bucket_name, public_range, vpc_network, vpc_range):
    """Enables and configures IP filtering rules on an existing bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # public_range = "192.0.2.0/24"
    # vpc_network = "projects/my-project/global/networks/my-network"
    # vpc_range = "10.0.0.0/24"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    ip_filter = bucket.ip_filter or IPFilter()
    ip_filter.mode = "Enabled"
    ip_filter.allow_all_service_agent_access = True
    ip_filter.allow_cross_org_vpcs = True

    if ip_filter.public_network_source is None:
        ip_filter.public_network_source = PublicNetworkSource(allowed_ip_cidr_ranges=[])
    if (
        public_range
        and public_range not in ip_filter.public_network_source.allowed_ip_cidr_ranges
    ):
        ip_filter.public_network_source.allowed_ip_cidr_ranges.append(public_range)

    if ip_filter.vpc_network_sources is None:
        ip_filter.vpc_network_sources = []

    existing_vpc = next(
        (v for v in ip_filter.vpc_network_sources if v.network == vpc_network),
        None,
    )
    if existing_vpc:
        if vpc_range and vpc_range not in existing_vpc.allowed_ip_cidr_ranges:
            existing_vpc.allowed_ip_cidr_ranges.append(vpc_range)
    elif vpc_network:
        vpc_sources = [vpc_range] if vpc_range else []
        ip_filter.vpc_network_sources.append(
            VpcNetworkSource(network=vpc_network, allowed_ip_cidr_ranges=vpc_sources)
        )

    bucket.ip_filter = ip_filter
    bucket.patch()

    print(f"Enabled IP filtering for bucket {bucket.name}.")
    return bucket


# [END storage_enable_ip_filtering]

if __name__ == "__main__":
    enable_ip_filtering(
        bucket_name=sys.argv[1],
        public_range=sys.argv[2],
        vpc_network=sys.argv[3],
        vpc_range=sys.argv[4],
    )
