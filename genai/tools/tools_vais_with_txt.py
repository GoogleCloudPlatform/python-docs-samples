# Copyright 2025 Google LLC
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


def generate_content(datastore: str) -> str:
    # [START googlegenaisdk_tools_vais_with_txt]
    from google import genai
    from google.genai.types import (
        GenerateContentConfig,
        HttpOptions,
        Retrieval,
        Tool,
        VertexAISearch,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Load Data Store ID from Vertex AI Search
    # datastore = "projects/111111111111/locations/global/collections/default_collection/dataStores/data-store-id"

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="How do I make an appointment to renew my driver's license?",
        config=GenerateContentConfig(
            tools=[
                # Use Vertex AI Search Tool
                Tool(
                    retrieval=Retrieval(
                        vertex_ai_search=VertexAISearch(
                            datastore=datastore,
                        )
                    )
                )
            ],
        ),
    )

    print(response.text)
    # Example response:
    # 'The process for making an appointment to renew your driver's license varies depending on your location. To provide you with the most accurate instructions...'
    # [END googlegenaisdk_tools_vais_with_txt]
    return response.text


if __name__ == "__main__":
    datastore = input("Data Store ID: ")
    generate_content(datastore)
