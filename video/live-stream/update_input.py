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

"""Google Cloud Live Stream sample for updating an input endpoint. This sample
    adds a preprocessing configuration to an existing input.
Example usage:
    python update_input.py --project_id <project-id> --location <location> --input_id <input-id>
"""

# [START livestream_update_input]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.protobuf import field_mask_pb2 as field_mask


def update_input(
    project_id: str, location: str, input_id: str
) -> live_stream_v1.types.Input:
    """Updates an input.
    Args:
        project_id: The GCP project ID.
        location: The location of the input.
        input_id: The user-defined input ID."""

    client = LivestreamServiceClient()

    name = f"projects/{project_id}/locations/{location}/inputs/{input_id}"

    input = live_stream_v1.types.Input(
        name=name,
        preprocessing_config=live_stream_v1.types.PreprocessingConfig(
            crop=live_stream_v1.types.PreprocessingConfig.Crop(
                top_pixels=5,
                bottom_pixels=5,
            )
        ),
    )
    update_mask = field_mask.FieldMask(paths=["preprocessing_config"])

    operation = client.update_input(input=input, update_mask=update_mask)
    response = operation.result(600)
    print(f"Updated input: {response.name}")

    return response


# [END livestream_update_input]

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
    update_input(
        args.project_id,
        args.location,
        args.input_id,
    )
