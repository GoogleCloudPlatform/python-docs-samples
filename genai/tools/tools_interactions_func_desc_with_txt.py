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


def create_interaction() -> str:
    # [START googlegenaisdk_interactions_tools_func_desc_with_txt]
    from google import genai
    from google.genai.interactions import Function

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    get_album_sales_tool = Function(
        name="get_album_sales",
        description="Gets the number of albums sold",
        parameters={
            "type": "object",
            "properties": {
                "albums": {
                    "type": "array",
                    "description": "List of albums",
                    "items": {
                        "description": "Album and its sales",
                        "type": "object",
                        "properties": {
                            "album_name": {
                                "type": "string",
                                "description": "Name of the music album",
                            },
                            "copies_sold": {
                                "type": "integer",
                                "description": "Number of copies sold",
                            },
                        },
                    },
                },
            },
        },
    )

    interaction = client.interactions.create(
        model=model_id,
        input=(
            'At Stellar Sounds, a music label, 2024 was a rollercoaster. "Echoes of the Night," a debut synth-pop album, '
            'surprisingly sold 350,000 copies, while veteran rock band "Crimson Tide\'s" latest, "Reckless Hearts," '
            'lagged at 120,000. Their up-and-coming indie artist, "Luna Bloom\'s" EP, "Whispers of Dawn," '
            'secured 75,000 sales. The biggest disappointment was the highly-anticipated rap album "Street Symphony" '
            "only reaching 100,000 units. Overall, Stellar Sounds moved over 645,000 units this year, revealing unexpected "
            "trends in music consumption."
        ),
        tools=[get_album_sales_tool],
    )

    function_calls = [
        {"name": step.name, "arguments": step.arguments}
        for step in interaction.steps
        if step.type == "function_call"
    ]

    print(function_calls)
    # [END googlegenaisdk_interactions_tools_func_desc_with_txt]
    return str(function_calls)


if __name__ == "__main__":
    create_interaction()
