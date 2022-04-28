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

"""Google Cloud Live Stream sample for creating an input endpoint. You send an
    input video stream to this endpoint.
Example usage:
    python create_input.py --project_id <project-id> --location <location> --input_id <input-id>
"""

# [START livestream_create_input]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)


def create_input(project_id: str, location: str, input_id: str) -> str:
    """Creates an input.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the input.
        input_id: The user-defined input ID."""

    client = LivestreamServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    input = live_stream_v1.types.Input(
        type_="RTMP_PUSH",
    )
    operation = client.create_input(parent=parent, input=input, input_id=input_id)
    response = operation.result(60)
    print(f"Input: {response.name}")

    return response


# [END livestream_create_input]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the input.",
        default="us-central1",
    )
    parser.add_argument(
        "--input_id",
        help="The user-defined input ID.",
        required=True,
    )
    args = parser.parse_args()
    create_input(
        args.project_id,
        args.location,
        args.input_id,
    )
