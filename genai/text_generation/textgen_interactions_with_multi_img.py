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
    # [START googlegenaisdk_interactions_textgen_with_multi_img]
    import base64
    from google import genai
    from google.genai.interactions import ImageContent, TextContent

    client = genai.Client()

    # Read content from GCS
    gcs_file_img_path = "gs://cloud-samples-data/generative-ai/image/scones.jpg"

    # Read content from a local file
    with open("test_data/latte.jpg", "rb") as f:
        local_file_img_bytes = f.read()
    local_file_img_b64 = base64.b64encode(local_file_img_bytes).decode("utf-8")

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            TextContent(text="Generate a list of all the objects contained in both images."),
            ImageContent(
                uri=gcs_file_img_path,
                mime_type="image/jpeg",
            ),
            ImageContent(
                data=local_file_img_b64,
                mime_type="image/jpeg",
            ),
        ],
    )
    print(interaction.output_text)
    # Example response:
    # Okay, here's the list of objects present in both images:
    # ...
    # [END googlegenaisdk_interactions_textgen_with_multi_img]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction()
