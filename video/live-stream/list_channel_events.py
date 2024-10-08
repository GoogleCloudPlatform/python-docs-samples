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

"""Google Cloud Live Stream sample for listing all events for a channel.
Example usage:
    python list_channel_events.py --project_id <project-id> --location <location> --channel_id <channel-id>
"""

# [START livestream_list_channel_events]

import argparse

from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
    pagers,
)


def list_channel_events(
    project_id: str, location: str, channel_id: str
) -> pagers.ListEventsPager:
    """Lists all events for a channel.
    Args:
        project_id: The GCP project ID.
        location: The location of the channel.
        channel_id: The user-defined channel ID."""

    client = LivestreamServiceClient()

    parent = f"projects/{project_id}/locations/{location}/channels/{channel_id}"
    page_result = client.list_events(parent=parent)
    print("Events:")

    responses = []
    for response in page_result:
        print(response.name)
        responses.append(response)

    return responses


# [END livestream_list_channel_events]

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
    list_channel_events(
        args.project_id,
        args.location,
        args.channel_id,
    )
