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
    # [START googlegenaisdk_imggen_mmflash_multiple_imgs_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=("Generate 3 images a cat sitting on a chair."),
        config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
    )
    saved_files = []
    image_counter = 1
    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        elif part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            filename = f"output_folder/example-cats-0{image_counter}.png"
            image.save(filename)
            saved_files.append(filename)
            image_counter += 1
    # Example response:
    #   Image 1: A fluffy calico cat with striking green eyes is perched elegantly on a vintage wooden
    #   chair with a woven seat. Sunlight streams through a nearby window, casting soft shadows and
    #   highlighting the cat's fur.
    #
    #   Image 2: A sleek black cat with intense yellow eyes is sitting upright on a modern, minimalist
    #   white chair. The background is a plain grey wall, putting the focus entirely on the feline's
    #   graceful posture.
    #
    #   Image 3: A ginger tabby cat with playful amber eyes is comfortably curled up asleep on a plush,
    #   oversized armchair upholstered in a soft, floral fabric. A corner of a cozy living room with a
    #   warm lamp in the background can be seen.
    # [END googlegenaisdk_imggen_mmflash_multiple_imgs_with_txt]
    return saved_files


if __name__ == "__main__":
    generate_content()
