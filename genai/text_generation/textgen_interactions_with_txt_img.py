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
    # [START googlegenaisdk_interactions_textgen_with_txt_img]
    from google import genai
    from google.genai.interactions import ImageContent, TextContent

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            TextContent(text="What is shown in this image?"),
            ImageContent(
                uri="gs://cloud-samples-data/generative-ai/image/scones.jpg",
                mime_type="image/jpeg",
            ),
        ],
    )
    print(interaction.output_text)
    # Example response:
    # The image shows a flat lay of blueberry scones arranged on parchment paper. There are ...
    # [END googlegenaisdk_interactions_textgen_with_txt_img]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()
