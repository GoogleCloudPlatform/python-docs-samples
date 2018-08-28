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

import entity_management
import entity_type_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
ENTITY_TYPE_DISPLAY_NAME = 'fake_entity_type_for_testing'
ENTITY_VALUE_1 = 'fake_entity_for_testing_1'
ENTITY_VALUE_2 = 'fake_entity_for_testing_2'
SYNONYMS = ['fake_synonym_for_testing_1', 'fake_synonym_for_testing_2']


def test_create_entity_type(capsys):
    entity_type_ids = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)

    assert len(entity_type_ids) == 0

    entity_type_management.create_entity_type(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME, 'KIND_MAP')
    out, _ = capsys.readouterr()

    assert 'display_name: "{}"'.format(ENTITY_TYPE_DISPLAY_NAME) in out

    entity_type_ids = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)

    assert len(entity_type_ids) == 1


def test_create_entity(capsys):
    entity_type_id = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)[0]

    entity_management.create_entity(
        PROJECT_ID, entity_type_id, ENTITY_VALUE_1, [])
    entity_management.create_entity(
        PROJECT_ID, entity_type_id, ENTITY_VALUE_2, SYNONYMS)

    entity_management.list_entities(PROJECT_ID, entity_type_id)
    out, _ = capsys.readouterr()

    assert 'Entity value: {}'.format(ENTITY_VALUE_1) in out
    assert 'Entity value: {}'.format(ENTITY_VALUE_2) in out
    for synonym in SYNONYMS:
        assert synonym in out


def test_delete_entity(capsys):
    entity_type_id = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)[0]

    entity_management.delete_entity(
        PROJECT_ID, entity_type_id, ENTITY_VALUE_1)
    entity_management.delete_entity(
        PROJECT_ID, entity_type_id, ENTITY_VALUE_2)

    entity_management.list_entities(PROJECT_ID, entity_type_id)
    out, _ = capsys.readouterr()

    assert out == ''


def test_delete_entity_type(capsys):
    entity_type_ids = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)

    for entity_type_id in entity_type_ids:
        entity_type_management.delete_entity_type(PROJECT_ID, entity_type_id)

    entity_type_ids = entity_type_management._get_entity_type_ids(
        PROJECT_ID, ENTITY_TYPE_DISPLAY_NAME)

    assert len(entity_type_ids) == 0
