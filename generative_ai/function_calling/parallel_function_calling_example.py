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

from vertexai.generative_models import ChatSession

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def parallel_function_calling_example() -> ChatSession:
    # [START generativeaionvertexai_function_calling_generate_parallel_calls]
    import vertexai

    from vertexai.generative_models import (
        FunctionDeclaration,
        GenerativeModel,
        Part,
        Tool,
    )

    # TODO(developer): Update & uncomment below line
    # PROJECT_ID = "your-project-id"

    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Specify a function declaration and parameters for an API request
    function_name = "get_current_weather"
    get_current_weather_func = FunctionDeclaration(
        name=function_name,
        description="Get the current weather in a given location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location for which to get the weather. \
                      It can be a city name, a city name and state, or a zip code. \
                      Examples: 'San Francisco', 'San Francisco, CA', '95616', etc.",
                },
            },
        },
    )

    # In this example, we'll use synthetic data to simulate a response payload from an external API
    def mock_weather_api_service(location: str) -> str:
        temperature = 25 if location == "San Francisco" else 35
        return f"""{{ "location": "{location}", "temperature": {temperature}, "unit": "C" }}"""

    # Define a tool that includes the above function
    tools = Tool(
        function_declarations=[get_current_weather_func],
    )

    # Initialize Gemini model
    model = GenerativeModel(
        model_name="gemini-1.5-pro-002",
        tools=[tools],
    )

    # Start a chat session
    chat_session = model.start_chat()
    response = chat_session.send_message(
        "Get weather details in New Delhi and San Francisco?"
    )

    function_calls = response.candidates[0].function_calls
    print("Suggested finction calls:\n", function_calls)

    if function_calls:
        api_responses = []
        for func in function_calls:
            if func.name == function_name:
                api_responses.append(
                    {
                        "content": mock_weather_api_service(
                            location=func.args["location"]
                        )
                    }
                )

        # Return the API response to Gemini
        response = chat_session.send_message(
            [
                Part.from_function_response(
                    name="get_current_weather",
                    response=api_responses[0],
                ),
                Part.from_function_response(
                    name="get_current_weather",
                    response=api_responses[1],
                ),
            ],
        )

        print(response.text)
        # Example response:
        # The current weather in New Delhi is 35°C. The current weather in San Francisco is 25°C.
        # [END generativeaionvertexai_function_calling_generate_parallel_calls]
        return response


if __name__ == "__main__":
    parallel_function_calling_example()
