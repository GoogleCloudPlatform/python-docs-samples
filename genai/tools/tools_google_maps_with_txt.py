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
    # [START googlegenaisdk_tools_google_maps_with_txt]
    from google import genai
    from google.genai.types import (
        ApiKeyConfig,
        AuthConfig,
        GenerateContentConfig,
        GoogleMaps,
        HttpOptions,
        Tool,
    )

    # TODO(developer): Update below line with your Google Maps API key
    GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Recommend a good restaurant in San Francisco.",
        config=GenerateContentConfig(
            tools=[
                # Use Google Maps Tool
                Tool(
                    google_maps=GoogleMaps(
                        auth_config=AuthConfig(
                            api_key_config=ApiKeyConfig(
                                api_key_string=GOOGLE_MAPS_API_KEY,
                            )
                        )
                    )
                )
            ],
        ),
    )

    print(response.text)
    # Example response:
    # 'San Francisco boasts a vibrant culinary scene...'
    # [END googlegenaisdk_tools_google_maps_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
