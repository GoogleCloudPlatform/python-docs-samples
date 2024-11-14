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


def tool_use() -> object:
    # [START generativeaionvertexai_claude_3_tool_use]
    # TODO(developer): Vertex AI SDK - uncomment below & run
    # pip3 install --upgrade --user google-cloud-aiplatform
    # gcloud auth application-default login
    # pip3 install -U 'anthropic[vertex]'
    from anthropic import AnthropicVertex

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    client = AnthropicVertex(project_id=PROJECT_ID, region="us-east5")
    message = client.messages.create(
        model="claude-3-5-sonnet-v2@20241022",
        max_tokens=1024,
        tools=[
            {
                "name": "text_search_places_api",
                "description": "returns information about a set of places based on a string",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "textQuery": {
                            "type": "string",
                            "description": "The text string on which to search",
                        },
                        "priceLevels": {
                            "type": "array",
                            "description": "Price levels to query places, value can be one of [PRICE_LEVEL_INEXPENSIVE, PRICE_LEVEL_MODERATE, PRICE_LEVEL_EXPENSIVE, PRICE_LEVEL_VERY_EXPENSIVE]",
                        },
                        "openNow": {
                            "type": "boolean",
                            "description": "whether those places are open for business.",
                        },
                    },
                    "required": ["textQuery"],
                },
            }
        ],
        messages=[
            {
                "role": "user",
                "content": "What are some affordable and good Italian restaurants open now in San Francisco??",
            }
        ],
    )
    print(message.model_dump_json(indent=2))
    # Example response:
    # {
    #   "id": "msg_vrtx_018pk1ykbbxAYhyWUdP1bJoQ",
    #   "content": [
    #     {
    #       "text": "To answer your question about affordable and good Italian restaurants
    #       that are currently open in San Francisco....
    # ...

    # [END generativeaionvertexai_claude_3_tool_use]
    return message


if __name__ == "__main__":
    tool_use()
