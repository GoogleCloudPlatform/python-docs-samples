#!/usr/bin/env python

# Copyright 2024 Google LLC.
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

"""Google Cloud Live Stream sample for deleting a channel clip.
Example usage:
    python delete_channel_clip.py --project_id <project-id> --location <location> \
        --channel_id <channel-id> --clip_id <clip-id>
"""

# [START livestream_delete_channel_clip]

import argparse

from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf import empty_pb2 as empty


def delete_channel_clip(
    project_id: str, location: str, channel_id: str, clip_id: str
) -> empty.Empty:
    """Deletes a channel clip.
    Args:
        project_id: The GCP project ID.
        location: The location of the channel.
        channel_id: The user-defined channel ID.
        clip_id: The user-defined clip ID."""

    client = LivestreamServiceClient()

    name = f"projects/{project_id}/locations/{location}/channels/{channel_id}/clips/{clip_id}"
    operation = client.delete_clip(name=name)
    response = operation.result(600)
    print("Deleted channel clip")

    return response


# [END livestream_delete_channel_clip]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the channel.",
        required=True,
    )
    parser.add_argument(
        "--channel_id",
        help="The user-defined channel ID.",
        required=True,
    )
    parser.add_argument(
        "--clip_id",
        help="The user-defined clip ID.",
        required=True,
    )
    args = parser.parse_args()
    delete_channel_clip(
        args.project_id,
        args.location,
        args.channel_id,
        args.clip_id,
    )
