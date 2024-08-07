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

"""Google Cloud Video Stitcher sample for creating a video on demand (VOD)
session in which to insert ads.
Example usage:
    python create_vod_session.py --project_id <project-id> \
        --location <location> --vod_config_id <vod-config-id>
"""

# [START videostitcher_create_vod_session]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_vod_session(
    project_id: str, location: str, vod_config_id: str
) -> stitcher_v1.types.VodSession:
    """Creates a VOD session. VOD sessions are ephemeral resources that expire
    after a few hours.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the session.
        vod_config_id: The user-defined VOD config ID to use to create the
                        session.

    Returns:
        The VOD session resource.
    """

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    vod_config_name = (
        f"projects/{project_id}/locations/{location}/vodConfigs/{vod_config_id}"
    )

    vod_session = stitcher_v1.types.VodSession(
        vod_config=vod_config_name, ad_tracking="SERVER"
    )

    response = client.create_vod_session(parent=parent, vod_session=vod_session)
    print(f"VOD session: {response.name}")
    return response


# [END videostitcher_create_vod_session]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the VOD session.",
        default="us-central1",
    )
    parser.add_argument(
        "--vod_config_id",
        help="The user-defined VOD config ID.",
        required=True,
    )
    args = parser.parse_args()
    create_vod_session(
        args.project_id,
        args.location,
        args.vod_config_id,
    )
