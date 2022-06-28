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

"""Google Cloud Live Stream sample for creating a channel with a backup input.
    A channel resource represents the processor that performs a user-defined
    "streaming" operation.
Example usage:
    python create_channel_with_backup_input.py --project_id <project-id> \
        --location <location> --channel_id <channel-id> \
        --primary_input_id <primary-input-id> \
        --backup_input_id <backup-input-id> --output_uri <uri>
"""

# [START livestream_create_channel_with_backup_input]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf import duration_pb2 as duration


def create_channel_with_backup_input(
    project_id: str,
    location: str,
    channel_id: str,
    primary_input_id: str,
    backup_input_id: str,
    output_uri: str,
) -> str:
    """Creates a channel.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the channel.
        channel_id: The user-defined channel ID.
        primary_input_id: The user-defined primary input ID.
        backup_input_id: The user-defined backup input ID.
        output_uri: Uri of the channel output folder in a Cloud Storage bucket."""

    client = LivestreamServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    primary_input = (
        f"projects/{project_id}/locations/{location}/inputs/{primary_input_id}"
    )
    backup_input = (
        f"projects/{project_id}/locations/{location}/inputs/{backup_input_id}"
    )
    name = f"projects/{project_id}/locations/{location}/channels/{channel_id}"

    channel = live_stream_v1.types.Channel(
        name=name,
        input_attachments=[
            live_stream_v1.types.InputAttachment(
                key="my-primary-input",
                input=primary_input,
                automatic_failover=live_stream_v1.types.InputAttachment.AutomaticFailover(
                    input_keys=["my-backup-input"],
                ),
            ),
            live_stream_v1.types.InputAttachment(
                key="my-backup-input",
                input=backup_input,
            ),
        ],
        output=live_stream_v1.types.Channel.Output(
            uri=output_uri,
        ),
        elementary_streams=[
            live_stream_v1.types.ElementaryStream(
                key="es_video",
                video_stream=live_stream_v1.types.VideoStream(
                    h264=live_stream_v1.types.VideoStream.H264CodecSettings(
                        profile="high",
                        width_pixels=1280,
                        height_pixels=720,
                        bitrate_bps=3000000,
                        frame_rate=30,
                    ),
                ),
            ),
            live_stream_v1.types.ElementaryStream(
                key="es_audio",
                audio_stream=live_stream_v1.types.AudioStream(
                    codec="aac", channel_count=2, bitrate_bps=160000
                ),
            ),
        ],
        mux_streams=[
            live_stream_v1.types.MuxStream(
                key="mux_video",
                elementary_streams=["es_video"],
                segment_settings=live_stream_v1.types.SegmentSettings(
                    segment_duration=duration.Duration(
                        seconds=2,
                    ),
                ),
            ),
            live_stream_v1.types.MuxStream(
                key="mux_audio",
                elementary_streams=["es_audio"],
                segment_settings=live_stream_v1.types.SegmentSettings(
                    segment_duration=duration.Duration(
                        seconds=2,
                    ),
                ),
            ),
        ],
        manifests=[
            live_stream_v1.types.Manifest(
                file_name="manifest.m3u8",
                type_="HLS",
                mux_streams=["mux_video", "mux_audio"],
                max_segment_count=5,
            ),
        ],
    )
    operation = client.create_channel(
        parent=parent, channel=channel, channel_id=channel_id
    )
    response = operation.result(60)
    print(f"Channel: {response.name}")

    return response


# [END livestream_create_channel_with_backup_input]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the channel.",
        default="us-central1",
    )
    parser.add_argument(
        "--channel_id",
        help="The user-defined channel ID.",
        required=True,
    )
    parser.add_argument(
        "--primary_input_id",
        help="The user-defined primary input ID.",
        required=True,
    )
    parser.add_argument(
        "--backup_input_id",
        help="The user-defined backup input ID.",
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        help="The Cloud Storage bucket (and optional folder) in which to save the livestream output.",
        required=True,
    )
    args = parser.parse_args()
    create_channel_with_backup_input(
        args.project_id,
        args.location,
        args.channel_id,
        args.primary_input_id,
        args.backup_input_id,
        args.output_uri,
    )
