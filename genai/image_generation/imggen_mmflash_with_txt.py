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
    # [START googlegenaisdk_imggen_mmflash_with_txt]
    import os
    from io import BytesIO

    from google import genai
    from google.genai.types import GenerateContentConfig, ImageConfig
    from PIL import Image

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-nano-banana-2.1",
        contents="Generate a high-contrast, grainy black and white street photography shot.",
        config=GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=ImageConfig(
                aspect_ratio="3:2",
                image_size="1K",
            ),
        ),
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            # Ensure the output directory exists
            output_dir = "output_folder"
            os.makedirs(output_dir, exist_ok=True)
            image.save(os.path.join(output_dir, "example-image.png"))

    # [END googlegenaisdk_imggen_mmflash_with_txt]
    return True


if __name__ == "__main__":
    generate_content()
