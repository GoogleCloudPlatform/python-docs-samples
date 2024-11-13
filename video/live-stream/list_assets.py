#!/usr/bin/env python

# Copyright 2023 Google LLC.
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

"""Google Cloud Live Stream sample for listing all assets in a location.
Example usage:
    python list_assets.py --project_id <project-id> --location <location>
"""

# [START livestream_list_assets]

import argparse

from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
    pagers,
)


def list_assets(project_id: str, location: str) -> pagers.ListAssetsPager:
    """Lists all assets in a location.
    Args:
        project_id: The GCP project ID.
        location: The location of the assets."""

    client = LivestreamServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    page_result = client.list_assets(parent=parent)
    print("Assets:")

    responses = []
    for response in page_result:
        print(response.name)
        responses.append(response)

    return responses


# [END livestream_list_assets]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the assets.",
        required=True,
    )
    args = parser.parse_args()
    list_assets(
        args.project_id,
        args.location,
    )
