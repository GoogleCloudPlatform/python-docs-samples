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

# [START storage_delete_ip_filtering_rules]
from google.cloud import storage


def delete_ip_filtering_rules(
    bucket_name, public_range_to_delete=None, vpc_network_to_delete=None
):
    """Selectively removes specific public CIDR ranges or VPC network sources."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # public_range_to_delete = "192.0.2.0/24"
    # vpc_network_to_delete = "projects/my-project/global/networks/my-network"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    if not bucket.ip_filter:
        print(f"Bucket {bucket_name} has no IP Filter configuration.")
        return bucket

    modified = False
    if public_range_to_delete and bucket.ip_filter.public_network_source:
        ranges = bucket.ip_filter.public_network_source.allowed_ip_cidr_ranges
        if ranges and public_range_to_delete in ranges:
            ranges.remove(public_range_to_delete)
            modified = True

    if vpc_network_to_delete and bucket.ip_filter.vpc_network_sources:
        initial_len = len(bucket.ip_filter.vpc_network_sources)
        bucket.ip_filter.vpc_network_sources = [
            v
            for v in bucket.ip_filter.vpc_network_sources
            if v.network != vpc_network_to_delete
        ]
        if len(bucket.ip_filter.vpc_network_sources) != initial_len:
            modified = True

    if modified:
        # Re-assign to a local variable and back to the bucket property to force
        # google-cloud-storage to register the nested changes for the patch() call.
        ip_filter = bucket.ip_filter
        bucket.ip_filter = ip_filter
        bucket.patch()
        print(f"Updated IP filtering rules for bucket {bucket_name}.")
    else:
        print("No changes were made to the bucket's IP filters.")

    return bucket


# [END storage_delete_ip_filtering_rules]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python storage_delete_ip_filtering_rules.py <bucket_name> [public_range_to_delete] [vpc_network_to_delete]"
        )
        sys.exit(1)
    delete_ip_filtering_rules(
        bucket_name=sys.argv[1],
        public_range_to_delete=sys.argv[2] if len(sys.argv) > 2 else None,
        vpc_network_to_delete=sys.argv[3] if len(sys.argv) > 3 else None,
    )
