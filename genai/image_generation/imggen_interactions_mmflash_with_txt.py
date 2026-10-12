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
    # [START googlegenaisdk_interactions_imggen_mmflash_with_txt]
    import base64
    import os
    from io import BytesIO

    from google import genai
    from PIL import Image

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-nano-banana-2.1",
        input="Generate an image of the Eiffel tower with fireworks in the background.",
        response_format={"type": "image"},
    )

    if interaction.output_text:
        print(interaction.output_text)

    if interaction.output_image:
        image = Image.open(BytesIO(base64.b64decode(interaction.output_image.data)))
        output_dir = "output_folder"
        os.makedirs(output_dir, exist_ok=True)
        image.save(os.path.join(output_dir, "example-image-eiffel-tower.png"))

    # [END googlegenaisdk_interactions_imggen_mmflash_with_txt]
    return True


if __name__ == "__main__":
    generate_content()
