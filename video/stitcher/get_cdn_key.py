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

"""Google Cloud Video Stitcher sample for getting a CDN key.
Example usage:
    python get_cdn_key.py --project_id <project_id> --location <location> \
        --cdn_key_id <cdn_key_id>
"""

# [START video_stitcher_get_cdn_key]

import argparse

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def get_cdn_key(project_id: str, location: str, cdn_key_id: str) -> str:
    """Gets a CDN key.
    Args:
        project_id: The GCP project ID.
        location: The location of the CDN key.
        cdn_key_id: The user-defined CDN key ID."""

    client = VideoStitcherServiceClient()

    name = f"projects/{project_id}/locations/{location}/cdnKeys/{cdn_key_id}"
    response = client.get_cdn_key(name=name)
    print(f"CDN key: {response.name}")
    return response


# [END video_stitcher_get_cdn_key]

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
    args = parser.parse_args()
    get_cdn_key(
        args.project_id,
        args.location,
        args.cdn_key_id,
    )
