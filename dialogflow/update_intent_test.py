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

PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT")
pytest.INTENT_ID = None
intent_suffix: str = str(uuid.uuid4())

def create_intent(project_id: str) -> str:
    intents_client: IntentsClient = IntentsClient()

    parent: str = AgentsClient.agent_path(project_id)

    intent: Intent = Intent()

    intent.display_name = f"fake_intent_{intent_suffix}"

    intents: Intent = intents_client.create_intent(request={"parent": parent, "intent": intent})

    return intents.name.split("/")[4]


@pytest.fixture(scope="function", autouse=True)
def setup_teardown() -> None:
    pytest.INTENT_ID = create_intent(project_id=PROJECT_ID)
    print("Created Intent in setUp")


def test_update_intent() -> None:

    fake_intent: str = f"fake_intent_{intent_suffix}"

    actual_response: Intent = update_intent(PROJECT_ID, pytest.INTENT_ID, fake_intent)
    expected_response: str = fake_intent

    intents_client: IntentsClient = IntentsClient()

    intents_client.delete_intent(name=actual_response.name)

    assert actual_response.display_name == expected_response
