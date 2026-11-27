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

import pytest
import resolve_auth_bindings


def test_resolve_auth_bindings(monkeypatch: pytest.MonkeyPatch) -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    mcp_server_id = os.environ.get("AGENTREGISTRY_TEST_MCP_SERVER_ID")
    if not project_id or not mcp_server_id:
        pytest.skip(
            "GOOGLE_CLOUD_PROJECT and AGENTREGISTRY_TEST_MCP_SERVER_ID must be set."
        )

    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", project_id)
    monkeypatch.setenv(
        "GOOGLE_CLOUD_LOCATION", os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    )

    agent = resolve_auth_bindings.resolve_auth_bindings(
        mcp_server_name=f"mcpServers/{mcp_server_id}",
    )
    assert agent.name == "maps_agent"
    assert len(agent.tools) == 1
