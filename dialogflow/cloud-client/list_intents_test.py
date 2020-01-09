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

import dialogflow_v2 as dialogflow
import pytest

import intent_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
INTENT_DISPLAY_NAME = 'intent_' \
                      + datetime.datetime.now().strftime("%Y%m%d%H%M%S")


@pytest.fixture(scope="function", autouse=True)
def setup():
    # Create an intent to list
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(PROJECT_ID)
    intent = dialogflow.types.Intent(display_name=INTENT_DISPLAY_NAME)
    response = intents_client.create_intent(parent, intent)
    intent_id = response.name.split('agent/intents/')[1]

    yield

    # Delete the created context
    intent_path = intents_client.intent_path(PROJECT_ID, intent_id)
    intents_client.delete_intent(intent_path)


def test_list_intents(capsys):
    intent_management.list_intents(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert INTENT_DISPLAY_NAME in out
