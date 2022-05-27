#!/usr/bin/env python

# Copyright 2022 Google Inc. All Rights Reserved.
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

"""Google Cloud Video Stitcher sample for creating a CDN key. A CDN key is used
to retrieve protected media.
Example usage:
    python create_cdn_key.py --project_id <project-id> --location <location> --cdn_key_id <cdn_key_id> \
        --hostname <hostname> [--gcdn_keyname <name> --gcdn_private_key <secret> | --akamai_token_key <token-key>]
"""

# [START video_stitcher_create_cdn_key]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_cdn_key(
    project_id: str,
    location: str,
    cdn_key_id: str,
    hostname: str,
    gcdn_keyname: str = None,
    gcdn_private_key: str = None,
    akamai_token_key: str = None,
) -> str:
    """Creates a Google Cloud or Akamai CDN key.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the CDN key.
        cdn_key_id: The user-defined CDN key ID.
        hostname: The hostname to which this CDN key applies.
        gcdn_keyname: Applies to a Google Cloud CDN key. A base64-encoded string secret.
        gcdn_private_key: Applies to a Google Cloud CDN key. Public name of the key.
        akamai_token_key: Applies to an Akamai CDN key. A base64-encoded string token key."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    cdn_key = stitcher_v1.types.CdnKey(
        name=cdn_key_id,
        hostname=hostname,
    )

    if akamai_token_key is not None:
        cdn_key.akamai_cdn_key = stitcher_v1.types.AkamaiCdnKey(
            token_key=akamai_token_key,
        )
    elif gcdn_keyname is not None:
        cdn_key.google_cdn_key = stitcher_v1.types.GoogleCdnKey(
            key_name=gcdn_keyname,
            private_key=gcdn_private_key,
        )

    response = client.create_cdn_key(
        parent=parent, cdn_key_id=cdn_key_id, cdn_key=cdn_key
    )
    print(f"CDN key: {response.name}")
    return response


# [END video_stitcher_create_cdn_key]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the CDN key.",
        default="us-central1",
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
        "--gcdn_keyname",
        help="Applies to a Google Cloud CDN key. The base64-encoded string secret.",
    )
    parser.add_argument(
        "--gcdn_private_key",
        help="Applies to a Google Cloud CDN key. Public name of the key.",
    )
    parser.add_argument(
        "--akamai_token_key",
        help="Applies to an Akamai CDN key. The base64-encoded string token key.",
    )
    args = parser.parse_args()
    create_cdn_key(
        args.project_id,
        args.location,
        args.cdn_key_id,
        args.hostname,
        args.gcdn_keyname,
        args.gcdn_private_key,
        args.akamai_token_key,
    )
