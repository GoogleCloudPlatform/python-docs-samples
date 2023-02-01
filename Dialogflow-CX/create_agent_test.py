# Copyright 2020, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test for create_agent"""

import os
import uuid

from google.cloud.dialogflowcx_v3.services.agents.client import AgentsClient
from google.cloud.dialogflowcx_v3.types.agent import DeleteAgentRequest

import pytest

from create_agent import create_agent

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
pytest.AGENT_PATH = ""


def delete_agent(name):
    agents_client = AgentsClient()
    request = DeleteAgentRequest(name=name)
    agents_client.delete_agent(request=request)


def test_create_agent():
    agentName = f"fake_agent_{uuid.uuid4()}"
    response = create_agent(PROJECT_ID, agentName)
    delete_agent(response.name)

    assert response.display_name == agentName
