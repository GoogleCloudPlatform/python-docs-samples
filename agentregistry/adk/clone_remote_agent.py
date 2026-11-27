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


def clone_remote_agent(
    agent_name: str = "projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID",
    model: str = "gemini-2.5-flash",
) -> tuple[LlmAgent, LlmAgent]:
    """Fetches a remote A2A agent once and clones it across orchestrators."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    registry = AgentRegistry(
        project_id=project_id,
        location=location,
    )

    # [START agentregistry_adk_clone_remote_agent]
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

    base_remote_agent = registry.get_remote_a2a_agent(
        agent_name=agent_name,
        httpx_client=httpx_client,
    )

    flight_orchestrator = LlmAgent(
        model=model,
        name="flight_orchestrator",
        sub_agents=[base_remote_agent.clone()],
    )

    hotel_orchestrator = LlmAgent(
        model=model,
        name="hotel_orchestrator",
        sub_agents=[base_remote_agent.clone()],
    )
    # [END agentregistry_adk_clone_remote_agent]
    return flight_orchestrator, hotel_orchestrator


if __name__ == "__main__":
    clone_remote_agent()
