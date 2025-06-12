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
    # [START googlegenaisdk_ctrlgen_with_nullable_schema]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "forecast": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "Day": {"type": "STRING", "nullable": True},
                        "Forecast": {"type": "STRING", "nullable": True},
                        "Temperature": {"type": "INTEGER", "nullable": True},
                        "Humidity": {"type": "STRING", "nullable": True},
                        "Wind Speed": {"type": "INTEGER", "nullable": True},
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

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=prompt,
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    print(response.text)
    # Example output:
    # {"forecast": [{"Day": "Sunday", "Forecast": "sunny", "Temperature": 77, "Wind Speed": 10, "Humidity": "50%"},
    #   {"Day": "Monday", "Forecast": "partly cloudy", "Temperature": 72, "Wind Speed": 15},
    #   {"Day": "Tuesday", "Forecast": "rain showers", "Temperature": 64, "Wind Speed": null, "Humidity": "70%"},
    #   {"Day": "Wednesday", "Forecast": "thunderstorms", "Temperature": 68, "Wind Speed": null},
    #   {"Day": "Thursday", "Forecast": "cloudy", "Temperature": 66, "Wind Speed": null, "Humidity": "60%"},
    #   {"Day": "Friday", "Forecast": "partly cloudy", "Temperature": 73, "Wind Speed": 12},
    #   {"Day": "Saturday", "Forecast": "sunny", "Temperature": 80, "Wind Speed": 8, "Humidity": "40%"}]}
    # [END googlegenaisdk_ctrlgen_with_nullable_schema]
    return response.text


if __name__ == "__main__":
    generate_content()
