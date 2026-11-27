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

from google.adk.integrations.agent_registry import AgentRegistry
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset


def auth_mcp_toolset(
    mcp_server_name: str = "mcpServers/SERVER_ID",
) -> McpToolset:
    """Retrieves an MCP toolset authenticated with Application Default Credentials."""
    # [START agentregistry_adk_auth_mcp_toolset]
    # Initialize the registry client
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    registry = AgentRegistry(
        project_id=project_id,
        location=location,
    )

    # Retrieve an MCP toolset using its resource name
    my_mcp_toolset = registry.get_mcp_toolset(mcp_server_name=mcp_server_name)
    # [END agentregistry_adk_auth_mcp_toolset]
    return my_mcp_toolset


if __name__ == "__main__":
    auth_mcp_toolset()
