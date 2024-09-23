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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def delete_reasoning_engine(reasoning_engine_id: str) -> None:
    # [START generativeaionvertexai_delete_reasoning_engine]
    import vertexai
    from vertexai.preview import reasoning_engines

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # reasoning_engine_id = "1234567890123456"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    reasoning_engine = reasoning_engines.ReasoningEngine(reasoning_engine_id)
    reasoning_engine.delete()
    # Example response:
    # Deleting ReasoningEngine:projects/[PROJECT_ID]/locations/us-central1/reasoningEngines/1234567890123456
    # ...
    # ... resource projects/[PROJECT_ID]/locations/us-central1/reasoningEngines/1234567890123456 deleted.

    # [END generativeaionvertexai_delete_reasoning_engine]


if __name__ == "__main__":
    delete_reasoning_engine("1234567890123456")
