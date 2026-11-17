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
    # [START googlegenaisdk_interactions_tools_func_def_with_txt]
    from google import genai
    from google.genai.interactions import Function

    def get_current_weather(location: str) -> str:
        """Example method. Returns the current weather.

        Args:
            location: The city and state, e.g. San Francisco, CA
        """
        weather_map: dict[str, str] = {
            "Boston, MA": "snowing",
            "San Francisco, CA": "foggy",
            "Seattle, WA": "raining",
            "Austin, TX": "hot",
            "Chicago, IL": "windy",
        }
        return weather_map.get(location, "unknown")

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    # Define function tool declaration for the Interactions API
    weather_tool = Function(
        name="get_current_weather",
        description="Returns the current weather for a given city and state.",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    )

    interaction = client.interactions.create(
        model=model_id,
        input="What is the weather like in Boston?",
        tools=[weather_tool],
    )

    # Check for function call step and execute it if requested
    for step in interaction.steps:
        if step.type == "function_call" and step.name == "get_current_weather":
            args = step.arguments or {}
            result = get_current_weather(**args)

            # Return function execution result back in a follow-up interaction
            interaction = client.interactions.create(
                model=model_id,
                previous_interaction_id=interaction.id,
                input=[
                    {
                        "type": "function_result",
                        "call_id": step.id,
                        "name": step.name,
                        "result": [{"type": "text", "text": result}],
                    }
                ],
            )
            break

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_tools_func_def_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction()
