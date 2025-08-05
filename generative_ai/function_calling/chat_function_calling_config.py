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


def generate_text() -> object:
    # [START generativeaionvertexai_gemini_chat_completions_function_calling_config]
    import vertexai
    import openai

    from google.auth import default, transport

    # TODO(developer): Update & uncomment below line
    # PROJECT_ID = "your-project-id"
    location = "us-central1"

    vertexai.init(project=PROJECT_ID, location=location)

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    auth_request = transport.requests.Request()
    credentials.refresh(auth_request)

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA or a zip code e.g. 95616",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
        }
    )
    messages.append({"role": "user", "content": "What is the weather in Boston, MA?"})

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    print("Function:", response.choices[0].message.tool_calls[0].id)
    print("Arguments:", response.choices[0].message.tool_calls[0].function.arguments)
    # Example response:
    # Function: get_current_weather
    # Arguments: {"location":"Boston"}
    # [END generativeaionvertexai_gemini_chat_completions_function_calling_config]

    return response


if __name__ == "__main__":
    generate_text()
