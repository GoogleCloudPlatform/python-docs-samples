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

import mcp_custom_headers
import pytest


def test_my_auth_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "test-api-key")
    headers = mcp_custom_headers.my_auth_headers(context=None)
    assert headers == {
        "Authorization": "Bearer test-api-key",
        "X-Custom-Context": "orchestrator-request",
    }


def test_get_external_mcp_toolset(monkeypatch: pytest.MonkeyPatch) -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    external_server_id = os.environ.get("AGENTREGISTRY_TEST_EXTERNAL_MCP_SERVER_ID")
    if not project_id or not external_server_id:
        pytest.skip(
            "GOOGLE_CLOUD_PROJECT and AGENTREGISTRY_TEST_EXTERNAL_MCP_SERVER_ID "
            "must be set."
        )

    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", project_id)
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", location)
    monkeypatch.setenv("API_KEY", "test-api-key")

    toolset = mcp_custom_headers.get_external_mcp_toolset(
        mcp_server_name=(
            f"projects/{project_id}/locations/{location}"
            f"/mcpServers/{external_server_id}"
        ),
    )
    assert toolset is not None
