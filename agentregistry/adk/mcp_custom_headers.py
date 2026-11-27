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

from google.adk.integrations.agent_registry import AgentRegistry
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset


# [START agentregistry_adk_mcp_custom_headers]
def my_auth_headers(context: Any) -> dict[str, str]:
    """Returns custom headers injected into MCP toolset requests."""
    external_api_key = os.environ.get("API_KEY", "")
    return {
        "Authorization": f"Bearer {external_api_key}",
        "X-Custom-Context": "orchestrator-request",
    }


def get_external_mcp_toolset(
    mcp_server_name: str = (
        "projects/PROJECT_ID/locations/LOCATION/mcpServers/EXTERNAL_SERVER_ID"
    ),
) -> McpToolset:
    """Initializes AgentRegistry with header_provider and fetches an MCP toolset."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize the registry client.
    # The header_provider is sent to the target MCP server during invocation,
    # not to authenticate against the Agent Registry API (which uses ADC).
    registry = AgentRegistry(
        project_id=project_id,
        location=location,
        header_provider=my_auth_headers,
    )

    external_mcp_toolset = registry.get_mcp_toolset(mcp_server_name=mcp_server_name)
    # [END agentregistry_adk_mcp_custom_headers]
    return external_mcp_toolset


if __name__ == "__main__":
    get_external_mcp_toolset()
