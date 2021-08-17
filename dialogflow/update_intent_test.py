# Copyright 2021 Google LLC
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

import os
import uuid

from google.cloud.dialogflow_v2.services.agents.client import AgentsClient
from google.cloud.dialogflow_v2.services.intents.client import IntentsClient
from google.cloud.dialogflow_v2.types.intent import Intent

import pytest

from update_intent import update_intent

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
pytest.INTENT_ID = None


def create_intent(project_id):
    intents_client = IntentsClient()

    parent = AgentsClient.agent_path(project_id)

    intent = Intent()

    intent.display_name = "fake_intent"

    intents = intents_client.create_intent(request={"parent": parent,  "intent": intent})

    return intents.name.split("/")[4]


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    pytest.INTENT_ID = create_intent(project_id=PROJECT_ID)
    print("Created Intent in setUp")


def test_update_intent():

    fake_intent = "fake_intent_{}".format(uuid.uuid4())

    actualResponse = update_intent(PROJECT_ID, pytest.INTENT_ID, fake_intent)
    expectedResponse = fake_intent

    intents_client = IntentsClient()

    intents_client.delete_intent(name=actualResponse.name)

    assert actualResponse.display_name == expectedResponse
