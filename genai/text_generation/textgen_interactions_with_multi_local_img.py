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


def create_interaction(image_path_1: str, image_path_2: str) -> str:
    # [START googlegenaisdk_interactions_textgen_with_multi_local_img]
    import base64
    from google import genai
    from google.genai.interactions import ImageContent, TextContent

    client = genai.Client()
    # TODO(Developer): Update the below file paths to your images
    # image_path_1 = "path/to/your/image1.jpg"
    # image_path_2 = "path/to/your/image2.jpg"
    with open(image_path_1, "rb") as f:
        image_1_bytes = f.read()
    with open(image_path_2, "rb") as f:
        image_2_bytes = f.read()

    image_1_b64 = base64.b64encode(image_1_bytes).decode("utf-8")
    image_2_b64 = base64.b64encode(image_2_bytes).decode("utf-8")

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            TextContent(text="Generate a list of all the objects contained in both images."),
            ImageContent(
                data=image_1_b64,
                mime_type="image/jpeg",
            ),
            ImageContent(
                data=image_2_b64,
                mime_type="image/jpeg",
            ),
        ],
    )
    print(interaction.output_text)
    # Example response:
    # Okay, here's a jingle combining the elements of both sets of images, focusing on ...
    # ...
    # [END googlegenaisdk_interactions_textgen_with_multi_local_img]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction(
        "./test_data/latte.jpg",
        "./test_data/scones.jpg",
    )
