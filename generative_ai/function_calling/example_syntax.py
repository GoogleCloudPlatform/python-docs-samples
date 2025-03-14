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

import vertexai

from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

vertexai.init(project=PROJECT_ID, location="us-central1")


def create_model_with_toolbox() -> GenerativeModel:
    # [START generativeaionvertexai_function_calling_example_syntax]
    from vertexai.generative_models import FunctionDeclaration, GenerationConfig, GenerativeModel, Tool

    gemini_model = GenerativeModel(
        "gemini-1.5-flash-002",
        generation_config=GenerationConfig(temperature=0),
        tools=[
            Tool(
                function_declarations=[
                    FunctionDeclaration(
                        name="get_current_weather",
                        description="Get the current weather in a given location",
                        parameters={
                            "type": "object",
                            "properties": {"location": {"type": "string", "description": "Location"}},
                        },
                    )
                ]
            )
        ],
    )
    # [END generativeaionvertexai_function_calling_example_syntax]
    return gemini_model


if __name__ == "__main__":
    create_model_with_toolbox()
