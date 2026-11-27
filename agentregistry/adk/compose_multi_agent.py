# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Iterator
import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.integrations.agent_registry import AgentRegistry
import google.auth
from google.auth.transport.requests import Request
import httpx


def compose_multi_agent(
    agent_name: str = "agents/AGENT_ID",
    mcp_server_name: str = "mcpServers/SERVER_ID",
    model: str = "gemini-2.5-flash",
) -> LlmAgent:
    """Initializes AgentRegistry and composes an orchestrator LlmAgent."""
    # [START agentregistry_adk_initialize_client]
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize the client
    registry = AgentRegistry(
        project_id=project_id,
        location=location,
    )
    # [END agentregistry_adk_initialize_client]

    # [START agentregistry_adk_compose_multi_agent]
    class GoogleAuth(httpx.Auth):
        def __init__(self) -> None:
            self.creds, _ = google.auth.default()

        def auth_flow(self, request: httpx.Request) -> Iterator[httpx.Request]:
            self.creds.before_request(
                Request(),
                request.method,
                str(request.url),
                request.headers,
            )
            yield request

    httpx_client = httpx.AsyncClient(
        auth=GoogleAuth(),
        timeout=httpx.Timeout(60.0),
    )
    my_remote_agent = registry.get_remote_a2a_agent(
        agent_name=agent_name,
        httpx_client=httpx_client,
    )
    my_mcp_toolset = registry.get_mcp_toolset(mcp_server_name=mcp_server_name)

    main_agent = LlmAgent(
        model=model,
        name="travel_orchestrator",
        instruction=(
            "You are a travel coordinator. You can use your subagents to book "
            "travel and your tools to query historical travel data."
        ),
        tools=[my_mcp_toolset],
        sub_agents=[my_remote_agent],
    )
    # [END agentregistry_adk_compose_multi_agent]
    return main_agent


if __name__ == "__main__":
    compose_multi_agent()
