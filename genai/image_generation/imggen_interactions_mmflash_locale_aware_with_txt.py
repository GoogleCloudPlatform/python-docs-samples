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
    # [START googlegenaisdk_interactions_imggen_mmflash_locale_aware_with_txt]
    import base64
    from io import BytesIO
    from google import genai
    from PIL import Image

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-nano-banana-2.1",
        input="Generate a photo of a breakfast meal.",
        response_format={"type": "image"},
    )

    if interaction.output_text:
        print(interaction.output_text)

    if interaction.output_image:
        image = Image.open(BytesIO(base64.b64decode(interaction.output_image.data)))
        image.save("output_folder/example-breakfast-meal.png")

    # [END googlegenaisdk_interactions_imggen_mmflash_locale_aware_with_txt]
    return "output_folder/example-breakfast-meal.png"


if __name__ == "__main__":
    generate_content()
