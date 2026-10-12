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


def generate_content() -> bool:
    # [START googlegenaisdk_interactions_imggen_mmflash_txt_and_img_with_txt]
    import base64
    from io import BytesIO
    import os
    from google import genai
    from PIL import Image

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-nano-banana-2.1",
        input=(
            "Generate an illustrated recipe for a paella. "
            "Create images to go alongside the text as you generate the recipe."
        ),
        response_format=[
            {"type": "text"},
            {"type": "image"},
        ],
    )

    os.makedirs("output_folder", exist_ok=True)
    img_counter = 1
    with open("output_folder/paella-recipe.md", "w") as fp:
        for step in interaction.steps:
            if step.type == "model_output":
                for content in step.content:
                    if content.type == "text":
                        fp.write(content.text)
                    elif content.type == "image":
                        image = Image.open(BytesIO(base64.b64decode(content.data)))
                        img_path = f"output_folder/example-image-{img_counter}.png"
                        image.save(img_path)
                        fp.write(f"![image]({img_path})\n")
                        img_counter += 1

        if img_counter == 1 and interaction.output_image:
            image = Image.open(BytesIO(base64.b64decode(interaction.output_image.data)))
            img_path = "output_folder/example-image-1.png"
            image.save(img_path)
            fp.write(f"![image]({img_path})\n")

    # [END googlegenaisdk_interactions_imggen_mmflash_txt_and_img_with_txt]
    return True


if __name__ == "__main__":
    generate_content()
