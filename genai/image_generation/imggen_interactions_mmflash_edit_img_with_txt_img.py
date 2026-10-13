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
    # [START googlegenaisdk_interactions_imggen_mmflash_edit_img_with_txt_img]
    import base64
    from io import BytesIO
    from google import genai
    from google.genai.interactions import ImageContent, ImageResponseFormat, TextContent
    from PIL import Image

    client = genai.Client()

    # Using an image of Eiffel tower, with fireworks in the background.
    with open("test_resources/example-image-eiffel-tower.png", "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode("utf-8")

    interaction = client.interactions.create(
        model="gemini-nano-banana-2.1",
        input=[
            ImageContent(data=b64_image, mime_type="image/png"),
            TextContent(text="Edit this image to make it look like a cartoon."),
        ],
        response_format=ImageResponseFormat(),
    )

    if interaction.output_text:
        print(interaction.output_text)

    if interaction.output_image:
        image = Image.open(BytesIO(base64.b64decode(interaction.output_image.data)))
        image.save("output_folder/bw-example-image.png")

    # [END googlegenaisdk_interactions_imggen_mmflash_edit_img_with_txt_img]
    return "output_folder/bw-example-image.png"


if __name__ == "__main__":
    generate_content()
