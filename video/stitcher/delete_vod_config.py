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

"""Google Cloud Video Stitcher sample for deleting a VOD config.
Example usage:
    python delete_vod_config.py --project_id <project-id> --location <location> \
        --vod_config_id <vod-config-id>
"""

# [START videostitcher_delete_vod_config]

import argparse

from google.cloud.video.stitcher_v1.services.video_stitcher_service import (
    VideoStitcherServiceClient,
)
from google.protobuf import empty_pb2 as empty


def delete_vod_config(
    project_id: str, location: str, vod_config_id: str
) -> empty.Empty:
    """Deletes a VOD config.
    Args:
        project_id: The GCP project ID.
        location: The location of the VOD config.
        vod_config_id: The user-defined VOD config ID."""

    client = VideoStitcherServiceClient()

    name = f"projects/{project_id}/locations/{location}/vodConfigs/{vod_config_id}"
    operation = client.delete_vod_config(name=name)
    response = operation.result()
    print("Deleted VOD config")
    return response


# [END videostitcher_delete_vod_config]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the VOD config.",
        required=True,
    )
    parser.add_argument(
        "--vod_config_id",
        help="The user-defined VOD config ID.",
        required=True,
    )
    args = parser.parse_args()
    delete_vod_config(
        args.project_id,
        args.location,
        args.vod_config_id,
    )
