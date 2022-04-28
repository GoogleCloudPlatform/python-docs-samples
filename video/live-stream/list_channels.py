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

"""Google Cloud Live Stream sample for listing all channels in a location.
Example usage:
    python list_channels.py --project_id <project-id> --location <location>
"""

# [START livestream_list_channels]

import argparse

from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)


def list_channels(project_id: str, location: str) -> list:
    """Lists all channels in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the channels."""

    client = LivestreamServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    page_result = client.list_channels(parent=parent)
    print("Channels:")

    responses = []
    for response in page_result:
        print(response.name)
        responses.append(response)

    return responses


# [END livestream_list_channels]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the channels.",
        required=True,
    )
    args = parser.parse_args()
    list_channels(
        args.project_id,
        args.location,
    )
