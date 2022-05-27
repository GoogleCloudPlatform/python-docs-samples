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

"""Google Cloud Video Stitcher sample for creating a live stream session in
which to insert ads.
Example usage:
    python create_live_session.py --project_id <project-id> \
        --location <location> --live_stream_uri <uri> --ad_tag_uri <uri> \
        --slate_id <slate-id>
"""

# [START video_stitcher_create_live_session]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_live_session(
    project_id: str, location: str, live_stream_uri: str, ad_tag_uri: str, slate_id: str
) -> str:
    """Creates a live session. Live sessions are ephemeral resources that expire
    after a few minutes.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the session.
        live_stream_uri: Uri of the livestream to stitch; this URI must reference either an MPEG-DASH
                    manifest (.mpd) file or an M3U playlist manifest (.m3u8) file.
        ad_tag_uri: Uri of the ad tag.
        slate_id: The user-defined slate ID of the default slate to use when no slates are specified in an ad break's message."""

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    # Create dictionaries and pass them to the LiveSession constructor
    ad_tag_map = {"default": stitcher_v1.AdTag(uri=ad_tag_uri)}

    live_session = stitcher_v1.types.LiveSession(
        source_uri=live_stream_uri, ad_tag_map=ad_tag_map, default_slate_id=slate_id
    )

    response = client.create_live_session(parent=parent, live_session=live_session)
    print(f"Live session: {response.name}")
    return response


# [END video_stitcher_create_live_session]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the live session.",
        default="us-central1",
    )
    parser.add_argument(
        "--live_stream_uri",
        help="The Uri of the livestream to stitch (.mpd or .m3u8 file) in double quotes.",
        required=True,
    )
    parser.add_argument(
        "--ad_tag_uri",
        help="Uri of the ad tag in double quotes.",
        required=True,
    )
    parser.add_argument(
        "--slate_id",
        help="The user-defined slate ID of the default slate.",
        required=True,
    )
    args = parser.parse_args()
    create_live_session(
        args.project_id,
        args.location,
        args.live_stream_uri,
        args.ad_tag_uri,
        args.slate_id,
    )
