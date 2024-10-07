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

"""Google Cloud Live Stream sample for creating an asset. You use an
    asset to create a slate.
Example usage:
    python create_asset.py --project_id <project-id> --location <location> \
        --asset_id <asset-id> --asset_uri <asset-uri>
"""

# [START livestream_create_asset]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)


def create_asset(
    project_id: str, location: str, asset_id: str, asset_uri: str
) -> live_stream_v1.types.Asset:
    """Creates an asset.
    Args:
        project_id: The GCP project ID.
        location: The location in which to create the asset.
        asset_id: The user-defined asset ID.
        asset_uri: The asset URI (e.g., 'gs://my-bucket/my-video.mp4')."""

    client = LivestreamServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    asset = live_stream_v1.types.Asset(
        video=live_stream_v1.types.Asset.VideoAsset(
            uri=asset_uri,
        )
    )
    operation = client.create_asset(parent=parent, asset=asset, asset_id=asset_id)
    response = operation.result(600)
    print(f"Asset: {response.name}")

    return response


# [END livestream_create_asset]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location in which to create the asset.",
        default="us-central1",
    )
    parser.add_argument(
        "--asset_id",
        help="The user-defined asset ID.",
        required=True,
    )
    parser.add_argument(
        "--asset_uri",
        help="The asset URI (e.g., 'gs://my-bucket/my-video.mp4').",
        required=True,
    )
    args = parser.parse_args()
    create_asset(
        args.project_id,
        args.location,
        args.asset_id,
        args.asset_uri,
    )
