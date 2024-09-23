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
import os

from vertexai.preview import reasoning_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_reasoning_engine(reasoning_engine_id: str) -> reasoning_engines.ReasoningEngine:
    # [START generativeaionvertexai_get_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # reasoning_engine_id = "1234567890123456"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)
    print(reasoning_engine)
    # Example response:
    # <vertexai.reasoning_engines._reasoning_engines.ReasoningEngine object at 0x757999a63c40>
    # resource name: projects/[PROJECT_ID]/locations/us-central1/reasoningEngines/1234567890123456

    # [END generativeaionvertexai_get_reasoning_engine]
    return reasoning_engine


if __name__ == "__main__":
    get_reasoning_engine("1234567890123456")
