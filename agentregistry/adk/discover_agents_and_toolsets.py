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
from typing import Any

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.integrations.agent_registry import AgentRegistry
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset


def discover_agents_and_toolsets(
    agent_name: str = "agents/AGENT_ID",
    mcp_server_name: str = "mcpServers/SERVER_ID",
    filter_str: str = 'skills.tags:"translation"',
) -> tuple[dict[str, Any], RemoteA2aAgent, McpToolset]:
    """Discovers agents by skill tag and fetches a remote agent and MCP toolset."""
    # [START agentregistry_adk_discover_agents_and_toolsets]
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    registry = AgentRegistry(
        project_id=project_id,
        location=location,
    )

    # Discover agents by a required A2A skill, for example, translation
    translator_agents = registry.list_agents(filter_str=filter_str)

    # Connect to a remote A2A agent using its resource name
    summarizer_agent = registry.get_remote_a2a_agent(agent_name=agent_name)

    # Retrieve an MCP toolset using its resource name
    bq_toolset = registry.get_mcp_toolset(mcp_server_name=mcp_server_name)
    # [END agentregistry_adk_discover_agents_and_toolsets]
    return translator_agents, summarizer_agent, bq_toolset


if __name__ == "__main__":
    discover_agents_and_toolsets()
