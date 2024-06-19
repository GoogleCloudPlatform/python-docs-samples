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

# [START aiplatform_claude_3_tool_use]
# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
# pip3 install -U 'anthropic[vertex]'

from anthropic import AnthropicVertex


def tool_use(project_id: str, region: str) -> object:
    client = AnthropicVertex(region=region, project_id=project_id)
    message = client.messages.create(
        model="claude-3-opus@20240229",
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
    return message


# [END aiplatform_claude_3_tool_use]


if __name__ == "__main__":
    tool_use()
