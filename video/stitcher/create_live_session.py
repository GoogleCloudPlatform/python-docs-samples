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

"""Google Cloud Video Stitcher sample for creating a live stream session in
which to insert ads.
Example usage:
    python create_live_session.py --project_id <project-id> \
        --location <location> --live_config_id <live-config-id>
"""

# [START videostitcher_create_live_session]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_live_session(
    project_id: str, location: str, live_config_id: str
) -> stitcher_v1.types.LiveSession:
    """Creates a live session. Live sessions are ephemeral resources that expire
    after a few minutes.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the session.
        live_config_id: The user-defined live config ID.

    Returns:
        The live session resource.
    """

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    live_config = (
        f"projects/{project_id}/locations/{location}/liveConfigs/{live_config_id}"
    )

    live_session = stitcher_v1.types.LiveSession(live_config=live_config)

    response = client.create_live_session(parent=parent, live_session=live_session)
    print(f"Live session: {response.name}")
    return response


# [END videostitcher_create_live_session]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the live session.",
        default="us-central1",
    )
    parser.add_argument(
        "--live_config_id",
        help="The user-defined live config ID.",
        required=True,
    )
    args = parser.parse_args()
    create_live_session(
        args.project_id,
        args.location,
        args.live_config_id,
    )
