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

import intent_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
INTENT_DISPLAY_NAME = 'intent_' \
                      + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
MESSAGE_TEXTS = [
    'fake_message_text_for_testing_1',
    'fake_message_text_for_testing_2'
]
TRAINING_PHRASE_PARTS = [
    'fake_training_phrase_part_1',
    'fake_training_phease_part_2'
]
pytest.INTENT_ID = None


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Delete the created context
    intents_client = dialogflow.IntentsClient()
    assert pytest.INTENT_ID is not None
    intent_path = intents_client.intent_path(PROJECT_ID, pytest.INTENT_ID)
    intents_client.delete_intent(intent_path)


def test_create_intent(capsys):
    intent_management.create_intent(PROJECT_ID, INTENT_DISPLAY_NAME,
                                    TRAINING_PHRASE_PARTS, MESSAGE_TEXTS)
    out, _ = capsys.readouterr()
    assert INTENT_DISPLAY_NAME in out

    pytest.INTENT_ID = out.split('agent/intents/')[1].split('"\n')[0]
