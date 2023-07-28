#!/usr/bin/env python

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Video Stitcher sample for updating an Akamai CDN key.
Example usage:
    python update_cdn_key_akamai.py --project_id <project-id> --location <location> \
        --cdn_key_id <cdn_key_id> --hostname <hostname> \
        --akamai_token_key <token-key>
"""

# [START videostitcher_update_cdn_key_akamai]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)
from google.protobuf import field_mask_pb2 as field_mask


def update_cdn_key_akamai(
    project_id: str,
    location: str,
    cdn_key_id: str,
    hostname: str,
    akamai_token_key: str,
) -> stitcher_v1.types.CdnKey:
    """Updates an Akamai CDN key.
    Args:
        project_id: The GCP project ID.
        location: The location of the CDN key.
        cdn_key_id: The user-defined CDN key ID.
        hostname: The hostname to which this CDN key applies.
        akamai_token_key: A base64-encoded string token key.

    Returns:
        The CDN key resource.
    """

    client = VideoStitcherServiceClient()

    name = f"projects/{project_id}/locations/{location}/cdnKeys/{cdn_key_id}"

    cdn_key = stitcher_v1.types.CdnKey(
        name=name,
        hostname=hostname,
        akamai_cdn_key=stitcher_v1.types.AkamaiCdnKey(
            token_key=akamai_token_key,
        ),
    )
    update_mask = field_mask.FieldMask(paths=["hostname", "akamai_cdn_key"])

    operation = client.update_cdn_key(cdn_key=cdn_key, update_mask=update_mask)
    response = operation.result()
    print(f"Updated CDN key: {response.name}")
    return response


# [END videostitcher_update_cdn_key_akamai]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the CDN key.",
        required=True,
    )
    parser.add_argument(
        "--cdn_key_id",
        help="The user-defined CDN key ID.",
        required=True,
    )
    parser.add_argument(
        "--hostname",
        help="The hostname to which this CDN key applies.",
        required=True,
    )
    parser.add_argument(
        "--akamai_token_key",
        help="The base64-encoded string token key.",
        required=True,
    )
    args = parser.parse_args()
    update_cdn_key_akamai(
        args.project_id,
        args.location,
        args.cdn_key_id,
        args.hostname,
        args.akamai_token_key,
    )
