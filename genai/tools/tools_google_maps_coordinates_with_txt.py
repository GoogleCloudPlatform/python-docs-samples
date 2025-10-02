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
    # [START googlegenaisdk_tools_google_maps_coordinates_with_txt]
    from google import genai
    from google.genai.types import (
        GenerateContentConfig,
        GoogleMaps,
        HttpOptions,
        Tool,
        ToolConfig,
        RetrievalConfig,
        LatLng
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Where can I get the best espresso near me?",
        config=GenerateContentConfig(
            tools=[
                # Use Google Maps Tool
                Tool(google_maps=GoogleMaps())
            ],
            tool_config=ToolConfig(
                retrieval_config=RetrievalConfig(
                    lat_lng=LatLng(  # Pass coordinates for location-aware grounding
                        latitude=40.7128,
                        longitude=-74.006
                    ),
                    language_code="en_US",  # Optional: localize Maps results
                ),
            ),
        ),
    )

    print(response.text)
    # Example response:
    # 'Here are some of the top-rated places to get espresso near you: ...'
    # [END googlegenaisdk_tools_google_maps_coordinates_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()