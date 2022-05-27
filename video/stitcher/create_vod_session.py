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

"""Google Cloud Video Stitcher sample for creating a video on demand (VOD)
session in which to insert ads.
Example usage:
    python create_vod_session.py --project_id <project-id> \
        --location <location> --source_uri <uri> --ad_tag_uri <uri>
"""

# [START video_stitcher_create_vod_session]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_vod_session(
    project_id: str, location: str, source_uri: str, ad_tag_uri: str
) -> str:
    """Creates a VOD session. VOD sessions are ephemeral resources that expire
    after a few hours.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the session.
        source_uri: Uri of the media to stitch; this URI must reference either an MPEG-DASH
                    manifest (.mpd) file or an M3U playlist manifest (.m3u8) file.
        ad_tag_uri: Uri of the ad tag."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    vod_session = stitcher_v1.types.VodSession(
        source_uri=source_uri, ad_tag_uri=ad_tag_uri
    )

    response = client.create_vod_session(parent=parent, vod_session=vod_session)
    print(f"VOD session: {response.name}")
    return response


# [END video_stitcher_create_vod_session]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the VOD session.",
        default="us-central1",
    )
    parser.add_argument(
        "--source_uri",
        help="The Uri of the media to stitch (.mpd or .m3u8 file) in double quotes.",
        required=True,
    )
    parser.add_argument(
        "--ad_tag_uri",
        help="Uri of the ad tag in double quotes.",
        required=True,
    )
    args = parser.parse_args()
    create_vod_session(
        args.project_id,
        args.location,
        args.source_uri,
        args.ad_tag_uri,
    )
