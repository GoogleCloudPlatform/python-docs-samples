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
    # [START googlegenaisdk_imggen_mmflash_locale_aware_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=("Generate a photo of a breakfast meal."),
        config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
    )
    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        elif part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save("output_folder/example-breakfast-meal.png")
    # Example response:
    #   Generates a photo of a vibrant and appetizing breakfast meal.
    #   The scene will feature a white plate with golden-brown pancakes
    #   stacked neatly, drizzled with rich maple syrup and ...
    # [END googlegenaisdk_imggen_mmflash_locale_aware_with_txt]
    return "output_folder/example-breakfast-meal.png"


if __name__ == "__main__":
    generate_content()
