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


def generate_content() -> int:
    # [START googlegenaisdk_imggen_mmflash_txt_and_img_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=(
            "Generate an illustrated recipe for a paella."
            "Create images to go alongside the text as you generate the recipe"
        ),
        config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
    )
    with open("paella-recipe.md", "w") as fp:
        for i, part in enumerate(response.candidates[0].content.parts):
            if part.text is not None:
                fp.write(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                image.save(f"example-image-{i+1}.png")
                fp.write(f"![image](./example-image-{i+1}.png)")
    # Example response:
    #  A markdown page for a Paella recipe(`paella-recipe.md`) has been generated.
    #   It includes detailed steps and several images illustrating the cooking process.
    # [END googlegenaisdk_imggen_mmflash_txt_and_img_with_txt]
    return i


if __name__ == "__main__":
    generate_content()
