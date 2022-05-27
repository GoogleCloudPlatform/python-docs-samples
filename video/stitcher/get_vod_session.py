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

"""Google Cloud Video Stitcher sample for getting a video on demand (VOD)
session.
Example usage:
    python get_vod_session.py --project_id <project-id> --location <location> \
        --session_id <session-id>
"""

# [START video_stitcher_get_vod_session]

import argparse

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def get_vod_session(project_id: str, location: str, session_id: str) -> str:
    """Gets a VOD session. VOD sessions are ephemeral resources that expire
    after a few hours.
    Args:
        project_id: The GCP project ID.
        location: The location of the session.
        session_id: The ID of the VOD session."""

    client = VideoStitcherServiceClient()

    name = client.vod_session_path(project_id, location, session_id)
    response = client.get_vod_session(name=name)
    print(f"VOD session: {response.name}")
    return response


# [END video_stitcher_get_vod_session]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location", help="The location of the VOD session.", required=True
    )
    parser.add_argument(
        "--session_id", help="The ID of the VOD session.", required=True
    )
    args = parser.parse_args()
    get_vod_session(args.project_id, args.location, args.session_id)
