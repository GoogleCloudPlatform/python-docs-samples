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
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=("Generate an image of the Eiffel tower with fireworks in the background."),
        config=GenerateContentConfig(
            response_modalities=[Modality.TEXT, Modality.IMAGE],
            candidate_count=1,
            safety_settings=[
                {"method": "PROBABILITY"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT"},
                {"threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        ),
    )
    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        elif part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save("output_folder/example-image-eiffel-tower.png")
    # Example response:
    #   I will generate an image of the Eiffel Tower at night, with a vibrant display of
    #   colorful fireworks exploding in the dark sky behind it. The tower will be
    #   illuminated, standing tall as the focal point of the scene, with the bursts of
    #   light from the fireworks creating a festive atmosphere.
    # [END googlegenaisdk_imggen_mmflash_with_txt]
    return True


if __name__ == "__main__":
    generate_content()
