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

import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.auth.credential_manager import CredentialManager
from google.adk.integrations.agent_identity import GcpAuthProvider
from google.adk.integrations.agent_registry import AgentRegistry


def resolve_auth_bindings(
    mcp_server_name: str = "mcpServers/SERVER_ID",
    model: str = "gemini-2.5-flash",
) -> LlmAgent:
    """Fetches an authenticated MCP toolset with resolved auth provider bindings."""
    # [START agentregistry_adk_resolve_auth_bindings]
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Register the auth provider
    CredentialManager.register_auth_provider(GcpAuthProvider())

    # Initialize the registry client
    registry = AgentRegistry(
        project_id=project_id,
        location=location,
    )

    # Fetch the registered MCP toolset.
    # The ADK applies the bindings configured in Agent Registry.
    my_mcp_toolset = registry.get_mcp_toolset(mcp_server_name=mcp_server_name)

    # Compose the agent
    maps_agent = LlmAgent(
        name="maps_agent",
        model=model,
        instruction=(
            "You are a local guide and navigation expert. Your goal is to "
            "provide accurate location information and directions."
        ),
        tools=[my_mcp_toolset],
    )
    # [END agentregistry_adk_resolve_auth_bindings]
    return maps_agent


if __name__ == "__main__":
    resolve_auth_bindings()
