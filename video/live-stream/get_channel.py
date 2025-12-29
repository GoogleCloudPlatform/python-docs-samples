#!/usr/bin/env python

# Copyright 2022 Google LLC.
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

"""Google Cloud Live Stream sample for getting a channel.
Example usage:
    python get_channel.py --project_id <project-id> --location <location> --channel_id <channel-id>
"""

# [START livestream_get_channel]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)


def get_channel(
    project_id: str, location: str, channel_id: str
) -> live_stream_v1.types.Channel:
    """Gets a channel.
    Args:
        project_id: The GCP project ID.
        location: The location of the channel.
        channel_id: The user-defined channel ID."""

    client = LivestreamServiceClient()

    name = f"projects/{project_id}/locations/{location}/channels/{channel_id}"
    response = client.get_channel(name=name)
    print(f"Channel: {response.name}")
    print(f"Creation time: {response.create_time}")
    if response.labels:
        print("Labels:")
        for key, value in response.labels.items():
            print(f"  {key}: {value}")
    print(f"Update time: {response.update_time}")
    print(f"Streaming state: {response.streaming_state.name}")
    if response.streaming_error:
        print(f"Streaming error: {response.streaming_error.message}")
    print(f"Active input: {response.active_input}")
    for attachment in response.input_attachments:
        print(f"Input attachment: {attachment.key}")
    print(f"Output URI: {response.output.uri}")
    print(f"Log config: {response.log_config.log_severity.name}")
    if response.elementary_streams:
        print("Elementary streams:")
        for stream in response.elementary_streams:
            print(f"  {stream.key}")
    if response.mux_streams:
        print("Mux streams:")
        for stream in response.mux_streams:
            print(f"  {stream.key}")
    if response.manifests:
        print("Manifests:")
        for manifest in response.manifests:
            print(f"  {manifest.file_name} ({manifest.type_.name})")

    return response


# [END livestream_get_channel]

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
    args = parser.parse_args()
    get_channel(
        args.project_id,
        args.location,
        args.channel_id,
    )
