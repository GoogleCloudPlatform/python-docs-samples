# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.cloud.dialogflowcx_v3.services.agents.client import AgentsClient
from google.cloud.dialogflowcx_v3.services.intents.client import IntentsClient
from google.cloud.dialogflowcx_v3.types.agent import Agent, DeleteAgentRequest
from google.cloud.dialogflowcx_v3.types.intent import CreateIntentRequest, Intent

import pytest

from update_intent import update_intent

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
pytest.INTENT_ID = None
pytest.AGENT_ID = None
pytest.PARENT = None


def create_agent(project_id, display_name):
    parent = "projects/" + project_id + "/locations/global"

    agents_client = AgentsClient()

    agent = Agent(
        display_name=display_name,
        default_language_code="en",
        time_zone="America/Los_Angeles",
    )

    response = agents_client.create_agent(request={"agent": agent, "parent": parent})

    return response


def delete_agent(name):
    agents_client = AgentsClient()
    agent = DeleteAgentRequest(name=name)
    agents_client.delete_agent(request=agent)


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    agentName = "temp_agent_" + str(uuid.uuid4())
    pytest.PARENT = create_agent(PROJECT_ID, agentName).name
    pytest.AGENT_ID = pytest.PARENT.split("/")[5]
    print("Created Agent in setUp")
    intentClient = IntentsClient()
    intent = Intent()

    intent.display_name = "fake_intent"

    req = CreateIntentRequest()
    req.parent = pytest.PARENT
    req.intent = intent

    pytest.INTENT_ID = intentClient.create_intent(request=req).name.split("/")[7]

    yield

    delete_agent(pytest.PARENT)


def test_fieldmaskTest():
    fake_intent = f"fake_intent_{uuid.uuid4()}"
    actualResponse = update_intent(
        PROJECT_ID, pytest.AGENT_ID, pytest.INTENT_ID, "global", fake_intent
    )

    assert actualResponse.display_name == fake_intent
