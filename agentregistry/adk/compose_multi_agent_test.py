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

import pytest

import compose_multi_agent


def test_compose_multi_agent(
    monkeypatch: pytest.MonkeyPatch,
    project_id: str,
    location: str,
    agent_id: str,
    mcp_server_id: str,
) -> None:
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", project_id)
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", location)

    orchestrator = compose_multi_agent.compose_multi_agent(
        agent_name=f"agents/{agent_id}",
        mcp_server_name=f"mcpServers/{mcp_server_id}",
    )

    assert orchestrator.name == "travel_orchestrator"
    assert len(orchestrator.sub_agents) == 1
    assert len(orchestrator.tools) == 1
