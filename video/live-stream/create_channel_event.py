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

"""Google Cloud Live Stream sample for creating a channel event. An event is a
    sub-resource of a channel, which can be scheduled by the user to execute
    operations on a channel resource without having to stop the channel.
Example usage:
    python create_channel_event.py --project_id <project-id> --location <location> \
        --channel_id <channel-id> --event_id <event-id>
"""

# [START livestream_create_channel_event]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf import duration_pb2 as duration


def create_channel_event(
    project_id: str, location: str, channel_id: str, event_id: str
) -> live_stream_v1.types.Event:
    """Creates a channel event.
    Args:
        project_id: The GCP project ID.
        location: The location of the channel.
        channel_id: The user-defined channel ID.
        event_id: The user-defined event ID."""

    client = LivestreamServiceClient()
    parent = f"projects/{project_id}/locations/{location}/channels/{channel_id}"
    name = f"projects/{project_id}/locations/{location}/channels/{channel_id}/events/{event_id}"

    event = live_stream_v1.types.Event(
        name=name,
        ad_break=live_stream_v1.types.Event.AdBreakTask(
            duration=duration.Duration(
                seconds=30,
            ),
        ),
        execute_now=True,
    )

    response = client.create_event(parent=parent, event=event, event_id=event_id)
    print(f"Channel event: {response.name}")

    return response


# [END livestream_create_channel_event]

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
        "--event_id",
        help="The user-defined event ID.",
        required=True,
    )
    args = parser.parse_args()
    create_channel_event(
        args.project_id,
        args.location,
        args.channel_id,
        args.event_id,
    )
