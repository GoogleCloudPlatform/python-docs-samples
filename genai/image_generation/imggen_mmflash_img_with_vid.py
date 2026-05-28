# Copyright 2026 Google LLC
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
    # [START googlegenaisdk_imggen_mmflash_img_with_vid]
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality, Part
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    # A video on 'The ABCs of agent building'
    video = "https://www.youtube.com/watch?v=rjoMZyxncUI"

    response = client.models.generate_content(
        model="gemini-3.1-flash-image",
        contents=[
            Part.from_uri(
                file_uri=video,
                mime_type="video/mp4"
            ), 
            "Generate an infographic of the topics covered in this video."
        ],
        config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
    )
    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        elif part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save("output_folder/video-image.png")

    # [END googlegenaisdk_imggen_mmflash_img_with_vid]
    return "output_folder/video-image.png"


if __name__ == "__main__":
    generate_content()
