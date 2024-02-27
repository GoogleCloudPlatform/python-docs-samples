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

# [START aiplatform_gemini_function_calling]
import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)


def generate_function_call(prompt: str, project_id: str, location: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Initialize Gemini model
    model = GenerativeModel("gemini-1.0-pro")

    # Specify a function declaration and parameters for an API request
    get_current_weather_func = FunctionDeclaration(
        name="get_current_weather",
        description="Get the current weather in a given location",
        # Function parameters are specified in OpenAPI JSON schema format
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Location"}},
        },
    )

    # Define a tool that includes the above get_current_weather_func
    weather_tool = Tool(
        function_declarations=[get_current_weather_func],
    )

    # Send a prompt and instruct the model to generate content using the Tool that you just created
    response_fc = model.generate_content(
        prompt,
        generation_config={"temperature": 0},
        tools=[weather_tool],
    )

    # Transform the structured data response into a Python dictionary
    function_name = response_fc.candidates[0].content.parts[0].function_call.name
    parameters = {}
    for key, value in (
        response_fc.candidates[0].content.parts[0].function_call.args.items()
    ):
        parameters[key] = value
    parameters

    # This is where you would use the function_name and parameters to make an API request to fetch the current weather.
    # Here we'll use synthetic data to simulate a response payload from an external API.
    api_response = """{ "location": "Boston, MA", "temperature": 38, "description": "Partly Cloudy",
                   "icon": "partly-cloudy", "humidity": 65, "wind": { "speed": 10, "direction": "NW" } }"""

    # Return the API response to Gemini so it can generate a model response or request another function call
    response = model.generate_content(
        [
            Content(
                role="user",
                parts=[
                    Part.from_text(prompt),
                ],
            ),
            Content(
                role="function",
                parts=[
                    Part.from_dict(
                        {
                            "function_call": {
                                "name": "get_current_weather",
                            }
                        }
                    )
                ],
            ),
            Content(
                role="function",
                parts=[
                    Part.from_function_response(
                        name="get_current_weather",
                        response={
                            "content": api_response,
                        },
                    )
                ],
            ),
        ],
        tools=[weather_tool],
    )
    # Get the model summary response
    summary = response.candidates[0].content.parts[0].text

    return summary, response, response_fc


# [END aiplatform_gemini_function_calling]
