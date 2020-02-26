# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import os
import uuid
import pytest

import dialogflow_v2 as dialogflow

import entity_type_management

PROJECT_ID = os.getenv("GCLOUD_PROJECT")
DISPLAY_NAME = "entity_type_{}".format(uuid.uuid4()).replace('-', '')[:30]
pytest.ENTITY_TYPE_ID = None


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Delete the created entity type
    entity_types_client = dialogflow.EntityTypesClient()
    assert pytest.ENTITY_TYPE_ID is not None
    entity_type_path = entity_types_client.entity_type_path(
        PROJECT_ID, pytest.ENTITY_TYPE_ID
    )
    entity_types_client.delete_entity_type(entity_type_path)


def test_create_entity_type(capsys):
    entity_type_management.create_entity_type(
        PROJECT_ID, DISPLAY_NAME, "KIND_MAP"
    )
    out, _ = capsys.readouterr()

    assert 'display_name: "{}"'.format(DISPLAY_NAME) in out

    # Save the entity id so that it can be deleted
    pytest.ENTITY_TYPE_ID = out.split("agent/entityTypes/")[1].split('"\n')[0]
