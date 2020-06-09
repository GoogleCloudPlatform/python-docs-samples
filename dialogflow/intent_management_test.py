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

import intent_management

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
INTENT_DISPLAY_NAME = 'test_{}'.format(uuid.uuid4())
MESSAGE_TEXTS = [
    'fake_message_text_for_testing_1',
    'fake_message_text_for_testing_2'
]
TRAINING_PHRASE_PARTS = [
    'fake_training_phrase_part_1',
    'fake_training_phease_part_2'
]


def test_create_intent(capsys):
    intent_management.create_intent(
        PROJECT_ID, INTENT_DISPLAY_NAME, TRAINING_PHRASE_PARTS,
        MESSAGE_TEXTS)

    intent_ids = intent_management._get_intent_ids(
        PROJECT_ID, INTENT_DISPLAY_NAME)

    assert len(intent_ids) == 1

    intent_management.list_intents(PROJECT_ID)

    out, _ = capsys.readouterr()

    assert INTENT_DISPLAY_NAME in out

    for message_text in MESSAGE_TEXTS:
        assert message_text in out


def test_delete_session_entity_type(capsys):
    intent_ids = intent_management._get_intent_ids(
        PROJECT_ID, INTENT_DISPLAY_NAME)

    for intent_id in intent_ids:
        intent_management.delete_intent(PROJECT_ID, intent_id)

    intent_management.list_intents(PROJECT_ID)
    out, _ = capsys.readouterr()

    assert INTENT_DISPLAY_NAME not in out

    intent_ids = intent_management._get_intent_ids(
        PROJECT_ID, INTENT_DISPLAY_NAME)

    assert len(intent_ids) == 0
