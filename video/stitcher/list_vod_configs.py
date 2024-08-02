#!/usr/bin/env python

# Copyright 2024 Google LLC
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

"""Google Cloud Video Stitcher sample for listing all VOD configs in a location.
Example usage:
    python list_vod_configs.py --project_id <project-id> --location <location>
"""

# [START videostitcher_list_vod_configs]

import argparse

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    pagers,
    VideoStitcherServiceClient,
)


def list_vod_configs(project_id: str, location: str) -> pagers.ListVodConfigsPager:
    """Lists all VOD configs in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the VOD configs.

    Returns:
        An iterable object containing VOD config resources.
    """

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_vod_configs(parent=parent)
    print("VOD configs:")
    for vod_config in response.vod_configs:
        print({vod_config.name})

    return response


# [END videostitcher_list_vod_configs]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the VOD configs.",
        required=True,
    )
    args = parser.parse_args()
    list_vod_configs(
        args.project_id,
        args.location,
    )
