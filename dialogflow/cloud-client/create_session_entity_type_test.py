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

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'session_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
ENTITY_TYPE_DISPLAY_NAME = 'test_type_' \
                           + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
ENTITY_VALUES = ['fake_entity_value_1', 'fake_entity_value_2']


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # Create an entity type to be used in session entity creation
    entity_types_client = dialogflow.EntityTypesClient()
    parent = entity_types_client.project_agent_path(PROJECT_ID)
    entity_type = dialogflow.types.EntityType(
        display_name=ENTITY_TYPE_DISPLAY_NAME,
        kind=dialogflow.enums.EntityType.Kind.KIND_MAP)

    response = entity_types_client.create_entity_type(parent, entity_type)
    entity_type_id = response.name.split('agent/entityTypes/')[1]

    yield

    # Delete the created entity type
    entity_type_path = entity_types_client.entity_type_path(
        PROJECT_ID, entity_type_id)
    entity_types_client.delete_entity_type(entity_type_path)


def test_create_session_entity_type(capsys):
    session_entity_type_management.create_session_entity_type(
        PROJECT_ID, SESSION_ID, ENTITY_VALUES, ENTITY_TYPE_DISPLAY_NAME,
        'ENTITY_OVERRIDE_MODE_SUPPLEMENT')

    out, _ = capsys.readouterr()

    assert SESSION_ID in out
    assert ENTITY_TYPE_DISPLAY_NAME in out
    for entity_value in ENTITY_VALUES:
        assert entity_value in out
