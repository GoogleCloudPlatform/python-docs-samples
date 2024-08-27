# Copyright 2024 Google LLC
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

import json
import os

import pytest

import list_locations

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_locations(capsys: pytest.fixture) -> None:
    # List the locations of the API
    r = list_locations.list_locations(project_id)
    locations = json.loads(r.text)

    found = False
    name = f"projects/{project_id}/locations/us-central1"

    for location in locations["locations"]:
        location_name = location["name"]
        if location_name == name:
            found = True
            break

    assert found
