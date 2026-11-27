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

import discover_agents_and_toolsets
import pytest


def test_discover_agents_and_toolsets(
    monkeypatch: pytest.MonkeyPatch,
    project_id: str,
    location: str,
    agent_id: str,
    mcp_server_id: str,
) -> None:
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", project_id)
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", location)

    agents_response, remote_agent, mcp_toolset = (
        discover_agents_and_toolsets.discover_agents_and_toolsets(
            agent_name=f"agents/{agent_id}",
            mcp_server_name=f"mcpServers/{mcp_server_id}",
        )
    )

    assert isinstance(agents_response, dict)
    assert remote_agent is not None
    assert mcp_toolset is not None
