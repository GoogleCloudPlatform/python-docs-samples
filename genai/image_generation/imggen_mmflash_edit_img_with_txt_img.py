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
    # [START googlegenaisdk_imggen_mmflash_edit_img_with_txt_img]
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    # Using an image of Eiffel tower, with fireworks in the background.
    image = Image.open("example-image.png")

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[image, "Edit this image to make it look like a cartoon."],
        config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
    )
    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        elif part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save("bw-example-image.png")
    # Example response:
    #  Here's the cartoon-style edit of the image:
    #  Cartoon-style edit:
    #  - Simplified the Eiffel Tower with bolder lines and slightly exaggerated proportions.
    #  - Brightened and saturated the colors of the sky, fireworks, and foliage for a more vibrant, cartoonish look.
    #  ....
    # [END googlegenaisdk_imggen_mmflash_edit_img_with_txt_img]
    return "bw-example-image.png"


if __name__ == "__main__":
    generate_content()
