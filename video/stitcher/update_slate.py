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

"""Google Cloud Video Stitcher sample for updating a slate.
Example usage:
    python update_slate.py --project_id <project-id> --location <location> \
        --slate_id <slate-id> --slate_uri <uri>
"""

# [START video_stitcher_update_slate]

import argparse

from google.cloud.video import stitcher_v1
from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)
from google.protobuf import field_mask_pb2 as field_mask


def update_slate(project_id: str, location: str, slate_id: str, slate_uri: str) -> str:
    """Updates a slate.
    Args:
        project_id: The GCP project ID.
        location: The location of the slate.
        slate_id: The existing slate's ID.
        slate_uri: Updated uri of the video slate; must be an MP4 video with at least one audio track."""

    client = VideoStitcherServiceClient()

    name = f"projects/{project_id}/locations/{location}/slates/{slate_id}"
    slate = stitcher_v1.types.Slate(
        name=name,
        uri=slate_uri,
    )
    update_mask = field_mask.FieldMask(paths=["uri"])

    response = client.update_slate(slate=slate, update_mask=update_mask)
    print(f"Updated slate: {response.name}")
    return response


# [END video_stitcher_update_slate]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the slate.",
        required=True,
    )
    parser.add_argument(
        "--slate_id",
        help="The existing slate's ID.",
        required=True,
    )
    parser.add_argument(
        "--slate_uri",
        help="Updated uri of the video slate; must be an MP4 video with at least one audio track.",
        required=True,
    )
    args = parser.parse_args()
    update_slate(
        args.project_id,
        args.location,
        args.slate_id,
        args.slate_uri,
    )
