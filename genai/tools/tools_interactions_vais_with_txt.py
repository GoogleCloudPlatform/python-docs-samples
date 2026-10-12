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


def generate_content(datastore: str) -> bool:
    # [START googlegenaisdk_interactions_tools_vais_with_txt]
    from google import genai

    client = genai.Client()

    # Load Data Store ID from Vertex AI Search
    # datastore = "projects/111111111111/locations/global/collections/default_collection/dataStores/data-store-id"

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="How do I make an appointment to renew my driver's license?",
        tools=[
            {
                "type": "retrieval",
                "vertex_ai_search_config": {
                    "datastores": [datastore],
                },
            }
        ],
    )

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_tools_vais_with_txt]
    return True


if __name__ == "__main__":
    datastore = input("Data Store ID: ")
    generate_content(datastore)
