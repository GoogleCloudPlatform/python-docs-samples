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

import entity_management

PROJECT_ID = os.getenv("GCLOUD_PROJECT")
DISPLAY_NAME = "entity_{}".format(uuid.uuid4()).replace('-', '')[:30]
ENTITY_VALUE_1 = "test_delete_entity_value"

pytest.ENTITY_TYPE_ID = None


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # Create an entity type
    entity_types_client = dialogflow.EntityTypesClient()
    parent = entity_types_client.project_agent_path(PROJECT_ID)
    entity_type = dialogflow.types.EntityType(
        display_name=DISPLAY_NAME,
        kind=dialogflow.enums.EntityType.Kind.KIND_MAP,
    )

    response = entity_types_client.create_entity_type(parent, entity_type)
    pytest.ENTITY_TYPE_ID = response.name.split("agent/entityTypes/")[1]

    # Create an entity inside the entity type
    entity_type_path = entity_types_client.entity_type_path(
        PROJECT_ID, pytest.ENTITY_TYPE_ID
    )
    entity = dialogflow.types.EntityType.Entity(
        value=ENTITY_VALUE_1, synonyms=[ENTITY_VALUE_1]
    )
    response = entity_types_client.batch_create_entities(
        entity_type_path, [entity]
    )
    response.result()

    yield

    # Delete the created entity type and its entities
    entity_types_client.delete_entity_type(entity_type_path)


def test_delete_entity(capsys):
    entity_management.delete_entity(
        PROJECT_ID, pytest.ENTITY_TYPE_ID, ENTITY_VALUE_1
    )

    entity_management.list_entities(PROJECT_ID, pytest.ENTITY_TYPE_ID)

    out, _ = capsys.readouterr()
    assert ENTITY_VALUE_1 not in out
