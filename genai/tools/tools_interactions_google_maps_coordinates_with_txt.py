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
    # [START googlegenaisdk_interactions_tools_google_maps_coordinates_with_txt]
    from google import genai
    from google.genai.interactions import GoogleMaps

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="Where can I get the best espresso near me?",
        tools=[GoogleMaps(latitude=40.7128, longitude=-74.006)],
    )

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_tools_google_maps_coordinates_with_txt]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()
