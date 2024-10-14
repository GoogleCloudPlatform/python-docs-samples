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

"""Google Cloud Live Stream sample for creating a channel clip. A channel clip
    is a sub-resource of a channel. You can use a channel clip to create video
    on demand (VOD) files from a live stream. These VOD files are saved to
    Cloud Storage.
Example usage:
    python create_channel_clip.py --project_id <project-id> --location <location> \
        --channel_id <channel-id> --clip_id <clip-id> --output_uri <uri>
"""

# [START livestream_create_channel_clip]

import argparse
import datetime

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf import timestamp_pb2


def create_channel_clip(
    project_id: str, location: str, channel_id: str, clip_id: str, output_uri: str
) -> live_stream_v1.types.Clip:
    """Creates a channel clip with a duration of 15 seconds.
    Args:
        project_id: The GCP project ID.
        location: The location of the channel.
        channel_id: The user-defined channel ID.
        clip_id: The user-defined clip ID.
        output_uri: Uri of the clip output in a Cloud Storage bucket."""

    client = LivestreamServiceClient()
    parent = f"projects/{project_id}/locations/{location}/channels/{channel_id}"
    name = f"projects/{project_id}/locations/{location}/channels/{channel_id}/clips/{clip_id}"
    # Create datetime values for now and 30 seconds earlier.
    now = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(
        seconds=10
    )
    earlier = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(
        seconds=30
    )
    # Create timestamps for the datetime values.
    markin_timestamp = timestamp_pb2.Timestamp()
    markin_timestamp.FromDatetime(earlier)
    markout_timestamp = timestamp_pb2.Timestamp()
    markout_timestamp.FromDatetime(now)

    clip = live_stream_v1.types.Clip(
        name=name,
        output_uri=output_uri,
        slices=[
            live_stream_v1.types.Clip.Slice(
                time_slice=live_stream_v1.types.Clip.TimeSlice(
                    markin_time=markin_timestamp.ToJsonString(),
                    markout_time=markout_timestamp.ToJsonString(),
                ),
            ),
        ],
        clip_manifests=[
            live_stream_v1.types.Clip.ClipManifest(
                manifest_key="manifest_hls",
            ),
        ],
    )

    operation = client.create_clip(parent=parent, clip=clip, clip_id=clip_id)
    response = operation.result(600)
    print(f"Channel clip: {response.name}")

    return response


# [END livestream_create_channel_clip]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the channel.",
        default="us-central1",
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
    parser.add_argument(
        "--output_uri",
        help="Uri of the clip output in a Cloud Storage bucket.",
        required=True,
    )
    args = parser.parse_args()
    create_channel_clip(
        args.project_id,
        args.location,
        args.channel_id,
        args.clip_id,
        args.output_uri,
    )
