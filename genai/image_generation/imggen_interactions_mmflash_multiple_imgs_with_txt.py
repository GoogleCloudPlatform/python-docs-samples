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


def generate_content() -> list[str]:
    # [START googlegenaisdk_interactions_imggen_mmflash_multiple_imgs_with_txt]
    import base64
    from io import BytesIO
    from google import genai
    from google.genai.interactions import ImageResponseFormat, TextResponseFormat
    from PIL import Image

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-nano-banana-2.1",
        input="Generate 3 images of a cat sitting on a chair.",
        response_format=[
            ImageResponseFormat(),
            TextResponseFormat(),
        ],
    )

    saved_files = []
    image_counter = 1

    for step in interaction.steps:
        if step.type == "model_output":
            for content in step.content:
                if content.type == "text":
                    print(content.text)
                elif content.type == "image":
                    image = Image.open(BytesIO(base64.b64decode(content.data)))
                    filename = f"output_folder/example-cats-0{image_counter}.png"
                    image.save(filename)
                    saved_files.append(filename)
                    image_counter += 1

    # Fallback to output_image if no step-level images collected
    if not saved_files and interaction.output_image:
        image = Image.open(BytesIO(base64.b64decode(interaction.output_image.data)))
        filename = "output_folder/example-cats-01.png"
        image.save(filename)
        saved_files.append(filename)

    # [END googlegenaisdk_interactions_imggen_mmflash_multiple_imgs_with_txt]
    return saved_files


if __name__ == "__main__":
    generate_content()
