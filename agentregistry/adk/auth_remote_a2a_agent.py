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

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.integrations.agent_registry import AgentRegistry
import google.auth
from google.auth.transport.requests import Request
import httpx


def auth_remote_a2a_agent(
    agent_name: str = "agents/AGENT_ID",
) -> RemoteA2aAgent:
    """Authenticates a remote A2A agent with Application Default Credentials."""
    # [START agentregistry_adk_auth_remote_a2a_agent]
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

    # Initialize the registry client
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    registry = AgentRegistry(
        project_id=project_id,
        location=location,
    )

    # Configure the HTTP client with GoogleAuth and a 60-second timeout
    httpx_client = httpx.AsyncClient(
        auth=GoogleAuth(),
        timeout=httpx.Timeout(60.0),
    )

    # Connect to a remote A2A agent using its resource name
    my_remote_agent = registry.get_remote_a2a_agent(
        agent_name=agent_name,
        httpx_client=httpx_client,
    )
    # [END agentregistry_adk_auth_remote_a2a_agent]
    return my_remote_agent


if __name__ == "__main__":
    auth_remote_a2a_agent()
