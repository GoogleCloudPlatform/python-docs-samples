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

"""Google Cloud Video Stitcher sample for listing the stitch details for a
video on demand (VOD) session.
Example usage:
    python list_vod_stitch_details.py --project_id <project-id> \
        --location <location> --session_id <session-id>
"""

# [START videostitcher_list_vod_stitch_details]

import argparse

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    pagers,
    VideoStitcherServiceClient,
)


def list_vod_stitch_details(
    project_id: str, location: str, session_id: str
) -> pagers.ListVodStitchDetailsPager:
    """Lists the stitch details for the specified VOD session.
    Args:
        project_id: The GCP project ID.
        location: The location of the session.
        session_id: The ID of the VOD session.

    Returns:
        An iterable object containing VOD stitch details resources.
    """

    client = VideoStitcherServiceClient()

    parent = client.vod_session_path(project_id, location, session_id)
    page_result = client.list_vod_stitch_details(parent=parent)
    print("VOD stitch details:")
    for response in page_result:
        print(response)

    return response


# [END videostitcher_list_vod_stitch_details]

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
    list_vod_stitch_details(args.project_id, args.location, args.session_id)
