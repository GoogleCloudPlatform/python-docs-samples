# Copyright 2017 Google LLC
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

import entity_type_management
import session_entity_type_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'test_session_{}'.format(uuid.uuid4())
ENTITY_TYPE_DISPLAY_NAME = 'test_{}'.format(uuid.uuid4()).replace('-', '')[:30]
ENTITY_VALUES = ['fake_entity_value_1', 'fake_entity_value_2']


def test_create_session_entity_type(capsys):
    # Create an entity type
    entity_type_management.create_entity_type(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME, 'KIND_MAP')

    session_entity_type_management.create_session_entity_type(
        PROJECT_ID, SESSION_ID, ENTITY_VALUES, ENTITY_TYPE_DISPLAY_NAME,
        'ENTITY_OVERRIDE_MODE_SUPPLEMENT')
    session_entity_type_management.list_session_entity_types(
        PROJECT_ID, SESSION_ID)

    out, _ = capsys.readouterr()

    assert SESSION_ID in out
    assert ENTITY_TYPE_DISPLAY_NAME in out
    for entity_value in ENTITY_VALUES:
        assert entity_value in out


def test_delete_session_entity_type(capsys):
    session_entity_type_management.delete_session_entity_type(
        PROJECT_ID, SESSION_ID, ENTITY_TYPE_DISPLAY_NAME)
    session_entity_type_management.list_session_entity_types(
        PROJECT_ID, SESSION_ID)

    out, _ = capsys.readouterr()
    assert ENTITY_TYPE_DISPLAY_NAME not in out
    for entity_value in ENTITY_VALUES:
        assert entity_value not in out

    # Clean up entity type
    entity_type_ids = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)
    for entity_type_id in entity_type_ids:
        entity_type_management.delete_entity_type(
            PROJECT_ID, entity_type_id)
