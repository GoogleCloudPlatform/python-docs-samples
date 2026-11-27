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

import vertexai
from vertexai.agent_engines.templates.a2a import default_a2a_agent


def deploy_agent_runtime(
    staging_bucket: str | None = None,
    display_name: str = "my-support-agent",
) -> Any:
    """Deploys an A2A agent to Vertex AI Agent Engine."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = vertexai.Client(project=project_id, location=location)
    my_a2a_agent = default_a2a_agent()

    config: dict[str, Any] = {
        "display_name": display_name,
        "description": "An agent that handles support tickets.",
        "requirements": ["google-cloud-aiplatform[agent_engines,a2a]"],
    }
    if staging_bucket:
        config["staging_bucket"] = staging_bucket

    # [START agentregistry_deploy_agent_runtime]
    # Create and deploy the agent
    # This action automatically registers the agent in Agent Registry
    remote_agent = client.agent_engines.create(
        agent=my_a2a_agent,
        config=config,
    )
    # [END agentregistry_deploy_agent_runtime]
    return remote_agent


if __name__ == "__main__":
    deploy_agent_runtime()
