#!/usr/bin/env python

# Copyright 2017 Google, Inc
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

import argparse

from google.cloud import kms_v1

# [START kms_quickstart]
def quickstart(project_id: str, location_id: str) -> kms_v1.services.key_management_service.pagers.ListKeyRingsPager:
    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the parent location name.
    location_name = f"projects/{project_id}/locations/{location_id}"

    # Call the API.
    key_rings = client.list_key_rings(request={"parent": location_name})

    # Example of iterating over key rings.
    for key_ring in key_rings:
        print(key_ring.name)

    return key_rings


# [END kms_quickstart]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("location_id", help="id of the KMS location")
    args = parser.parse_args()

    quickstart(args.project_id, args.location_id)
