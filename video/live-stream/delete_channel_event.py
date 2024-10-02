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

"""Google Cloud Live Stream sample for deleting a channel event.
Example usage:
    python delete_channel_event.py --project_id <project-id> --location <location> \
        --channel_id <channel-id> --event_id <event-id>
"""

# [START livestream_delete_channel_event]

import argparse

from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)


def delete_channel_event(
    project_id: str, location: str, channel_id: str, event_id: str
) -> None:
    """Deletes a channel event.
    Args:
        project_id: The GCP project ID.
        location: The location of the channel.
        channel_id: The user-defined channel ID.
        event_id: The user-defined event ID."""

    client = LivestreamServiceClient()

    name = f"projects/{project_id}/locations/{location}/channels/{channel_id}/events/{event_id}"
    response = client.delete_event(name=name)
    print("Deleted channel event")

    return response


# [END livestream_delete_channel_event]

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
        "--event_id",
        help="The user-defined event ID.",
        required=True,
    )
    args = parser.parse_args()
    delete_channel_event(
        args.project_id,
        args.location,
        args.channel_id,
        args.event_id,
    )
