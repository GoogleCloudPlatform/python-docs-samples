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


def generate_content(PROJECT_ID: str, REGION: str, MODEL_ID: str) -> object:
    # [START generativeaionvertexai_function_calling_basic]
    import vertexai
    from vertexai.generative_models import (
        FunctionDeclaration,
        GenerativeModel,
        GenerationConfig,
        Part,
        Tool,
    )

    vertexai.init(project=PROJECT_ID, location=REGION)

    # Specify a function declaration and parameters for an API request
    get_current_weather_func = FunctionDeclaration(
        name="get_current_weather",
        description="Get the current weather in a given location",
        # Function parameters are specified in OpenAPI JSON schema format
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA or a zip code e.g. 95616"}},
        },
    )

    # Define a tool that includes the above get_current_weather_func
    weather_tool = Tool(
        function_declarations=[get_current_weather_func],
    )

    model = GenerativeModel(
        MODEL_ID, generation_config={"temperature": 0}, tools=[weather_tool]
    )
    response = model.generate_content("What is the weather in Boston?")

    print(response)
    # [END generativeaionvertexai_function_calling_basic]

    return response