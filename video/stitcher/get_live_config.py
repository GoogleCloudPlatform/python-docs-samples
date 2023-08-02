#!/usr/bin/env python

# Copyright 2023 Google LLC
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

"""Google Cloud Video Stitcher sample for getting a live config.
Example usage:
    python get_live_config.py --project_id <project-id> --location <location> \
        --live_config_id <live-config-id>
"""

# [START videostitcher_get_live_config]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def get_live_config(
    project_id: str, location: str, live_config_id: str
) -> stitcher_v1.types.LiveConfig:
    """Gets a live config.
    Args:
        project_id: The GCP project ID.
        location: The location of the live config.
        live_config_id: The user-defined live config ID.

    Returns:
        The live config resource.
    """

    client = VideoStitcherServiceClient()

    name = f"projects/{project_id}/locations/{location}/liveConfigs/{live_config_id}"
    response = client.get_live_config(name=name)
    print(f"Live config: {response.name}")
    return response


# [END videostitcher_get_live_config]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the live config.",
        required=True,
    )
    parser.add_argument(
        "--live_config_id",
        help="The user-defined live config ID.",
        required=True,
    )
    args = parser.parse_args()
    get_live_config(
        args.project_id,
        args.location,
        args.live_config_id,
    )
