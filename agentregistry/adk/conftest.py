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


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def location() -> str:
    return os.environ.get("GOOGLE_CLOUD_LOCATION", "global")


@pytest.fixture()
def agent_id() -> str:
    value = os.environ.get("AGENTREGISTRY_TEST_AGENT_ID")
    if not value:
        pytest.skip("AGENTREGISTRY_TEST_AGENT_ID environment variable not set.")
    return value


@pytest.fixture()
def mcp_server_id() -> str:
    value = os.environ.get("AGENTREGISTRY_TEST_MCP_SERVER_ID")
    if not value:
        pytest.skip("AGENTREGISTRY_TEST_MCP_SERVER_ID environment variable not set.")
    return value


@pytest.fixture()
def staging_bucket() -> str:
    value = os.environ.get("AGENTREGISTRY_TEST_STAGING_BUCKET")
    if not value:
        pytest.skip("AGENTREGISTRY_TEST_STAGING_BUCKET environment variable not set.")
    return value
