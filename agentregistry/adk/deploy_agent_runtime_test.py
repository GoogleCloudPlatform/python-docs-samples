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

import uuid

import pytest
import vertexai

import deploy_agent_runtime


def test_deploy_agent_runtime(
    monkeypatch: pytest.MonkeyPatch,
    project_id: str,
    staging_bucket: str,
) -> None:
    location = "us-central1"
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", project_id)
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", location)

    display_name = f"agentregistry-test-{uuid.uuid4().hex[:8]}"
    remote_agent = None
    try:
        remote_agent = deploy_agent_runtime.deploy_agent_runtime(
            staging_bucket=staging_bucket,
            display_name=display_name,
        )
        assert remote_agent.api_resource.name
    finally:
        if remote_agent is not None and getattr(remote_agent, "api_resource", None):
            client = vertexai.Client(project=project_id, location=location)
            client.agent_engines.delete(
                name=remote_agent.api_resource.name,
                force=True,
            )
