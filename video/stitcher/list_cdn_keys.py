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

"""Google Cloud Video Stitcher sample for listing all CDN keys in a location.
Example usage:
    python list_cdn_keys.py --project_id <project-id> --location <location>
"""

# [START video_stitcher_list_cdn_keys]

import argparse

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def list_cdn_keys(project_id: str, location: str) -> str:
    """Lists all CDN keys in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the CDN keys."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_cdn_keys(parent=parent)
    print("CDN keys:")
    for cdn_key in response.cdn_keys:
        print({cdn_key.name})

    return response


# [END video_stitcher_list_cdn_keys]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the CDN keys.",
        required=True,
    )
    args = parser.parse_args()
    list_cdn_keys(
        args.project_id,
        args.location,
    )
