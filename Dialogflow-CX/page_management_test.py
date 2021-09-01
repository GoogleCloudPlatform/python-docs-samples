# Copyright 2021, Google LLC
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

import asyncio
from copy import Error
import os
import uuid

from google.cloud.dialogflowcx_v3.services.agents.client import AgentsClient
from google.cloud.dialogflowcx_v3.types.agent import Agent, DeleteAgentRequest

import pytest

from page_management import create_page, delete_page, list_page

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
pytest.AGENT_ID = None
pytest.PARENT = None
pytest.CREATED_PAGE = None
pytest.PAGE_ID = None


def delete_agent(name):
    agents_client = AgentsClient()
    agent = DeleteAgentRequest(name=name)
    agents_client.delete_agent(request=agent)


@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    loop = asyncio.new_event_loop()
    agentName = "temp_agent_" + str(uuid.uuid4())

    parent = "projects/" + PROJECT_ID + "/locations/global"

    agents_client = AgentsClient()

    agent = Agent(
        display_name=agentName,
        default_language_code="en",
        time_zone="America/Los_Angeles",
    )

    response = agents_client.create_agent(request={"agent": agent, "parent": parent})
    pytest.PARENT = response.name

    pytest.AGENT_ID = pytest.PARENT.split("/")[5]
    print("Created Agent in setUp")

    yield

    delete_agent(pytest.PARENT)
    loop.close()


def test_create_page(loop: asyncio.AbstractEventLoop):
    pytest.CREATED_PAGE = f"fake_page_{uuid.uuid4()}"
    actualResponse = loop.run_until_complete(
        create_page(
            PROJECT_ID,
            pytest.AGENT_ID,
            "00000000-0000-0000-0000-000000000000",
            "global",
            pytest.CREATED_PAGE,
        )
    )

    pytest.PAGE_ID = actualResponse.name.split("/")[9]
    assert actualResponse.display_name == pytest.CREATED_PAGE


def test_list_page(loop: asyncio.AbstractEventLoop):
    actualResponse = loop.run_until_complete(
        list_page(
            PROJECT_ID,
            pytest.AGENT_ID,
            "00000000-0000-0000-0000-000000000000",
            "global",
        )
    )

    assert pytest.PAGE_ID in str(actualResponse)


def test_delete_page(loop: asyncio.AbstractEventLoop):
    try:
        loop.run_until_complete(
            delete_page(
                PROJECT_ID,
                pytest.AGENT_ID,
                "00000000-0000-0000-0000-000000000000",
                pytest.PAGE_ID,
                "global",
            )
        )
    except Error:
        pytest.fail("Unexpected MyError ..")
