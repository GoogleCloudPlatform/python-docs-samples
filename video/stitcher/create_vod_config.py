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

"""Google Cloud Video Stitcher sample for creating a VOD config. VOD
configs are used to configure VOD sessions.
Example usage:
    python create_vod_config.py --project_id <project-id> --location <location> \
        --vod_config_id <vod-config-id> --vod_uri <uri> --ad_tag_uri <uri>
"""

# [START videostitcher_create_vod_config]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)


def create_vod_config(
    project_id: str,
    location: str,
    vod_config_id: str,
    vod_uri: str,
    ad_tag_uri: str,
) -> stitcher_v1.types.VodConfig:
    """Creates a VOD config.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the VOD config.
        vod_config_id: The user-defined VOD config ID.
        vod_uri: URI of the VOD to stitch; this URI must reference either an
                    MPEG-DASH manifest (.mpd) file or an M3U playlist manifest
                    (.m3u8) file.
        ad_tag_uri: Uri of the ad tag.

    Returns:
        The VOD config resource.
    """

    client = VideoStitcherServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    vod_config = stitcher_v1.types.VodConfig(
        source_uri=vod_uri,
        ad_tag_uri=ad_tag_uri,
    )

    operation = client.create_vod_config(
        parent=parent, vod_config_id=vod_config_id, vod_config=vod_config
    )
    response = operation.result()
    print(f"VOD config: {response.name}")
    return response


# [END videostitcher_create_vod_config]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the VOD config.",
        default="us-central1",
    )
    parser.add_argument(
        "--vod_config_id",
        help="The user-defined VOD config ID.",
        required=True,
    )
    parser.add_argument(
        "--vod_uri",
        help="The URI of the VOD stream to stitch (.mpd or .m3u8 file) in double quotes.",
        required=True,
    )
    parser.add_argument(
        "--ad_tag_uri",
        help="URI of the ad tag in double quotes.",
        required=True,
    )
    args = parser.parse_args()
    create_vod_config(
        args.project_id,
        args.location,
        args.vod_config_id,
        args.vod_uri,
        args.ad_tag_uri,
    )
