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


def generate_content() -> str:
    # [START googlegenaisdk_tools_func_desc_with_txt]
    from google import genai
    from google.genai.types import (
        FunctionDeclaration,
        GenerateContentConfig,
        HttpOptions,
        Tool,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.0-flash-001"

    get_album_sales = FunctionDeclaration(
        name="get_album_sales",
        description="Gets the number of albums sold",
        # Function parameters are specified in JSON schema format
        parameters={
            "type": "OBJECT",
            "properties": {
                "albums": {
                    "type": "ARRAY",
                    "description": "List of albums",
                    "items": {
                        "description": "Album and its sales",
                        "type": "OBJECT",
                        "properties": {
                            "album_name": {
                                "type": "STRING",
                                "description": "Name of the music album",
                            },
                            "copies_sold": {
                                "type": "INTEGER",
                                "description": "Number of copies sold",
                            },
                        },
                    },
                },
            },
        },
    )

    sales_tool = Tool(
        function_declarations=[get_album_sales],
    )

    response = client.models.generate_content(
        model=model_id,
        contents='At Stellar Sounds, a music label, 2024 was a rollercoaster. "Echoes of the Night," a debut synth-pop album, '
        'surprisingly sold 350,000 copies, while veteran rock band "Crimson Tide\'s" latest, "Reckless Hearts," '
        'lagged at 120,000. Their up-and-coming indie artist, "Luna Bloom\'s" EP, "Whispers of Dawn," '
        'secured 75,000 sales. The biggest disappointment was the highly-anticipated rap album "Street Symphony" '
        "only reaching 100,000 units. Overall, Stellar Sounds moved over 645,000 units this year, revealing unexpected "
        "trends in music consumption.",
        config=GenerateContentConfig(
            tools=[sales_tool],
            temperature=0,
        ),
    )

    print(response.function_calls)
    # Example response:
    # [FunctionCall(
    #     id=None,
    #     name="get_album_sales",
    #     args={
    #         "albums": [
    #             {"album_name": "Echoes of the Night", "copies_sold": 350000},
    #             {"copies_sold": 120000, "album_name": "Reckless Hearts"},
    #             {"copies_sold": 75000, "album_name": "Whispers of Dawn"},
    #             {"copies_sold": 100000, "album_name": "Street Symphony"},
    #         ]
    #     },
    # )]
    # [END googlegenaisdk_tools_func_desc_with_txt]
    return str(response.function_calls[0])


if __name__ == "__main__":
    generate_content()
