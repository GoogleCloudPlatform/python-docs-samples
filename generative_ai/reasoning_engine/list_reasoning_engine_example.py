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

from typing import List

from vertexai.preview import reasoning_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_reasoning_engines() -> List[reasoning_engines.ReasoningEngine]:
    # [START generativeaionvertexai_list_reasoning_engines]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reasoning_engine_list = reasoning_engines.ReasoningEngine.list()
    print(reasoning_engine_list)
    # Example response:
    # [<vertexai.reasoning_engines._reasoning_engines.ReasoningEngine object at 0x71a0e5cb99c0>
    # resource name: projects/123456789/locations/us-central1/reasoningEngines/111111111111111111,
    # <vertexai.reasoning_engines._reasoning_engines.ReasoningEngine object at 0x71a0e5cbac80>
    # resource name: projects/123456789/locations/us-central1/reasoningEngines/222222222222222222]

    # [END generativeaionvertexai_list_reasoning_engines]
    return reasoning_engine_list


if __name__ == "__main__":
    list_reasoning_engines()
