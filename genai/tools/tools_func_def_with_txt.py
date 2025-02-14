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
    # [START googlegenaisdk_tools_func_def_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

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

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.0-flash-001"

    response = client.models.generate_content(
        model=model_id,
        contents="What is the weather like in Boston?",
        config=GenerateContentConfig(
            tools=[get_current_weather],
            temperature=0,
        ),
    )

    print(response.text)
    # Example response:
    # The weather in Boston is sunny.
    # [END googlegenaisdk_tools_func_def_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
