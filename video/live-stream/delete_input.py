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

"""Google Cloud Live Stream sample for deleting an input.
Example usage:
    python delete_input.py --project_id <project-id> --location <location> --input_id <input-id>
"""

# [START livestream_delete_input]

import argparse

from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf import empty_pb2 as empty


def delete_input(project_id: str, location: str, input_id: str) -> empty.Empty:
    """Deletes an input.
    Args:
        project_id: The GCP project ID.
        location: The location of the input.
        input_id: The user-defined input ID."""

    client = LivestreamServiceClient()

    name = f"projects/{project_id}/locations/{location}/inputs/{input_id}"
    operation = client.delete_input(name=name)
    response = operation.result(600)
    print("Deleted input")

    return response


# [END livestream_delete_input]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the input.",
        required=True,
    )
    parser.add_argument(
        "--input_id",
        help="The user-defined input ID.",
        required=True,
    )
    args = parser.parse_args()
    delete_input(
        args.project_id,
        args.location,
        args.input_id,
    )
