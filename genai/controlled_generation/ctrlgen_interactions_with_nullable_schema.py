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
    # [START googlegenaisdk_interactions_ctrlgen_with_nullable_schema]
    from google import genai
    from google.genai.interactions import TextResponseFormat

    response_schema = {
        "type": "object",
        "properties": {
            "forecast": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "Day": {"type": "string", "nullable": True},
                        "Forecast": {"type": "string", "nullable": True},
                        "Temperature": {"type": "integer", "nullable": True},
                        "Humidity": {"type": "string", "nullable": True},
                        "Wind Speed": {"type": "integer", "nullable": True},
                    },
                    "required": ["Day", "Temperature", "Forecast", "Wind Speed"],
                },
            }
        },
    }

    prompt = """
        The week ahead brings a mix of weather conditions.
        Sunday is expected to be sunny with a temperature of 77°F and a humidity level of 50%. Winds will be light at around 10 km/h.
        Monday will see partly cloudy skies with a slightly cooler temperature of 72°F and the winds will pick up slightly to around 15 km/h.
        Tuesday brings rain showers, with temperatures dropping to 64°F and humidity rising to 70%.
        Wednesday may see thunderstorms, with a temperature of 68°F.
        Thursday will be cloudy with a temperature of 66°F and moderate humidity at 60%.
        Friday returns to partly cloudy conditions, with a temperature of 73°F and the Winds will be light at 12 km/h.
        Finally, Saturday rounds off the week with sunny skies, a temperature of 80°F, and a humidity level of 40%. Winds will be gentle at 8 km/h.
    """

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        response_format=TextResponseFormat(
            mime_type="application/json",
            schema=response_schema,
        ),
    )

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_ctrlgen_with_nullable_schema]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction()
