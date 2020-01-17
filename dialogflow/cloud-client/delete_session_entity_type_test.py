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

import datetime
import os
import pytest

import dialogflow_v2 as dialogflow

import session_entity_type_management

PROJECT_ID = os.getenv("GCLOUD_PROJECT")
SESSION_ID = "session_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
ENTITY_TYPE_DISPLAY_NAME = "session_type_" + datetime.datetime.now().strftime(
    "%Y%m%d%H%M%S"
)
ENTITY_VALUES = ["fake_entity_value_1", "fake_entity_value_2"]
pytest.ENTITY_TYPE_ID = None


@pytest.fixture(scope="function", autouse=True)
def setup():
    # Create an entity type for session deletion
    entity_types_client = dialogflow.EntityTypesClient()
    parent = entity_types_client.project_agent_path(PROJECT_ID)
    entity_type = dialogflow.types.EntityType(
        display_name=ENTITY_TYPE_DISPLAY_NAME,
        kind=dialogflow.enums.EntityType.Kind.KIND_MAP,
    )

    response = entity_types_client.create_entity_type(parent, entity_type)
    entity_type_id = response.name.split("agent/entityTypes/")[1]

    # Create a session entity type
    session_entity_types_client = dialogflow.SessionEntityTypesClient()
    session_path = session_entity_types_client.session_path(
        PROJECT_ID, SESSION_ID
    )
    session_entity_type_name = session_entity_types_client.session_entity_type_path(
        PROJECT_ID, SESSION_ID, ENTITY_TYPE_DISPLAY_NAME
    )
    entities = [
        dialogflow.types.EntityType.Entity(value=value, synonyms=[value])
        for value in ENTITY_VALUES
    ]
    session_entity_type = dialogflow.types.SessionEntityType(
        name=session_entity_type_name,
        entity_override_mode="ENTITY_OVERRIDE_MODE_OVERRIDE",
        entities=entities,
    )
    session_entity_types_client.create_session_entity_type(
        session_path, session_entity_type
    )

    yield

    # Delete the created entity type
    entity_type_path = entity_types_client.entity_type_path(
        PROJECT_ID, entity_type_id
    )
    entity_types_client.delete_entity_type(entity_type_path)


def test_delete_session_entity_type(capsys):
    session_entity_type_management.delete_session_entity_type(
        PROJECT_ID, SESSION_ID, ENTITY_TYPE_DISPLAY_NAME
    )

    session_entity_type_management.list_session_entity_types(
        PROJECT_ID, SESSION_ID
    )
    out, _ = capsys.readouterr()
    assert ENTITY_TYPE_DISPLAY_NAME not in out
