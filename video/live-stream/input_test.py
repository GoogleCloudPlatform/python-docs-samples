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

import os
import uuid

from google.api_core.exceptions import FailedPrecondition, NotFound
import pytest

import create_input
import delete_input
import get_input
import list_inputs
import update_input
import utils

project_name = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
input_id = f"my-python-test-input-{uuid.uuid4()}"


def test_input_operations(capsys: pytest.fixture) -> None:
    # Clean up old resources in the test project
    responses = list_inputs.list_inputs(project_name, location)
    for response in responses:
        next_input_id = response.name.rsplit("/", 1)[-1]
        if utils.is_resource_stale(response.create_time):
            try:
                delete_input.delete_input(project_name, location, next_input_id)
            except FailedPrecondition as e:
                print(f"Ignoring FailedPrecondition, details: {e}")
            except NotFound as e:
                print(f"Ignoring NotFound, details: {e}")

    input_name_project_id = (
        f"projects/{project_name}/locations/{location}/inputs/{input_id}"
    )

    # Tests

    create_input.create_input(project_name, location, input_id)
    out, _ = capsys.readouterr()
    assert input_name_project_id in out

    list_inputs.list_inputs(project_name, location)
    out, _ = capsys.readouterr()
    assert input_name_project_id in out

    response = update_input.update_input(project_name, location, input_id)
    out, _ = capsys.readouterr()
    assert input_name_project_id in out
    assert response.preprocessing_config.crop.top_pixels == 5

    get_input.get_input(project_name, location, input_id)
    out, _ = capsys.readouterr()
    assert input_name_project_id in out

    delete_input.delete_input(project_name, location, input_id)
    out, _ = capsys.readouterr()
    assert "Deleted input" in out
