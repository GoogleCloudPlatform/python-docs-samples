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
    # [START googlegenaisdk_interactions_textgen_with_gcs_audio]
    from google import genai
    from google.genai.interactions import AudioContent, TextContent

    client = genai.Client()
    prompt = """
    Provide a concise summary of the main points in the audio file.
    """
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            AudioContent(
                uri="gs://cloud-samples-data/generative-ai/audio/pixel.mp3",
                mime_type="audio/mpeg",
            ),
            TextContent(text=prompt),
        ],
    )
    print(interaction.output_text)
    # Example response:
    # Here's a summary of the main points from the audio file:

    # The Made by Google podcast discusses the Pixel feature drops with product managers Aisha Sheriff and De Carlos Love.  The key idea is that devices should improve over time, with a connected experience across phones, watches, earbuds, and tablets.
    # [END googlegenaisdk_interactions_textgen_with_gcs_audio]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction()
