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

import os
import uuid

from google.api_core.exceptions import FailedPrecondition, NotFound
from google.protobuf import empty_pb2 as empty
import pytest

import create_asset
import delete_asset
import get_asset
import list_assets
import utils

project_name = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
asset_id = f"my-python-test-asset-{uuid.uuid4()}"
asset_uri = "gs://cloud-samples-data/media/ForBiggerEscapes.mp4"


def test_asset_operations(capsys: pytest.fixture) -> None:
    # Clean up old resources in the test project
    responses = list_assets.list_assets(project_name, location)
    for response in responses:
        next_asset_id = response.name.rsplit("/", 1)[-1]
        if utils.is_resource_stale(response.create_time):
            try:
                delete_asset.delete_asset(project_name, location, next_asset_id)
            except FailedPrecondition as e:
                print(f"Ignoring FailedPrecondition, details: {e}")
            except NotFound as e:
                print(f"Ignoring NotFound, details: {e}")

    asset_name_project_id = (
        f"projects/{project_name}/locations/{location}/assets/{asset_id}"
    )

    # Tests

    response = create_asset.create_asset(project_name, location, asset_id, asset_uri)
    assert asset_name_project_id in response.name

    list_assets.list_assets(project_name, location)
    out, _ = capsys.readouterr()
    assert asset_name_project_id in out

    response = get_asset.get_asset(project_name, location, asset_id)
    assert asset_name_project_id in response.name

    response = delete_asset.delete_asset(project_name, location, asset_id)
    assert response == empty.Empty()
