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

"""Google Cloud Video Stitcher sample for creating a live config. Live
configs are used to configure live sessions.
Example usage:
    python create_live_config.py --project_id <project-id> --location <location> \
        --live_config_id <live-config-id> --live_stream_uri <uri> --ad_tag_uri <uri> \
        --slate_id <id>
"""

# [START videostitcher_create_live_config]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_live_config(
    project_id: str,
    location: str,
    live_config_id: str,
    live_stream_uri: str,
    ad_tag_uri: str,
    slate_id: str,
) -> stitcher_v1.types.LiveConfig:
    """Creates a live config.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the live config.
        live_config_id: The user-defined live config ID.
        live_stream_uri: Uri of the livestream to stitch; this URI must reference either an MPEG-DASH
                    manifest (.mpd) file or an M3U playlist manifest (.m3u8) file.
        ad_tag_uri: Uri of the ad tag.
        slate_id: The user-defined slate ID of the default slate to use when no slates are specified in an ad break's message.

    Returns:
        The live config resource.
    """

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    default_slate = f"projects/{project_id}/locations/{location}/slates/{slate_id}"

    live_config = stitcher_v1.types.LiveConfig(
        source_uri=live_stream_uri,
        ad_tag_uri=ad_tag_uri,
        ad_tracking="SERVER",
        stitching_policy="CUT_CURRENT",
        default_slate=default_slate,
    )

    operation = client.create_live_config(
        parent=parent, live_config_id=live_config_id, live_config=live_config
    )
    response = operation.result()
    print(f"Live config: {response.name}")
    return response


# [END videostitcher_create_live_config]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the live config.",
        default="us-central1",
    )
    parser.add_argument(
        "--live_config_id",
        help="The user-defined live config ID.",
        required=True,
    )
    parser.add_argument(
        "--live_stream_uri",
        help="The uri of the livestream to stitch (.mpd or .m3u8 file) in double quotes.",
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
    create_live_config(
        args.project_id,
        args.location,
        args.live_config_id,
        args.live_stream_uri,
        args.ad_tag_uri,
        args.slate_id,
    )
