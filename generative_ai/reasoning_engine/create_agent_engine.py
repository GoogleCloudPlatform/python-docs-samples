# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START generativeaionvertexai_create_agent_engine]
import vertexai


def create_agent_engine_with_memorybank_config(
    project_id: str,
    location: str,
    model: str = "gemini-1.5-flash",
) -> object:
    """Creates an Agent Engine instance with Memory Bank configuration."""
    vertexai.init(project=project_id, location=location)
    client = vertexai.Client()

    agent_engine = client.agent_engines.create(
        config={
            "context_spec": {
                "memory_bank_config": {
                    "generation_config": {
                        "model": f"projects/{project_id}/locations/{location}/publishers/google/models/{model}"
                    }
                }
            }
        }
    )
    print(f"Created Agent Engine: {agent_engine.api_resource.name}")
    return agent_engine
# [END generativeaionvertexai_create_agent_engine]
