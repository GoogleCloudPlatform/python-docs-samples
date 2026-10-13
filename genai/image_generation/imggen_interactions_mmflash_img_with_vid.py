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
    # [START googlegenaisdk_interactions_imggen_mmflash_img_with_vid]
    import base64
    from io import BytesIO
    from google import genai
    from google.genai.interactions import ImageResponseFormat, TextContent, VideoContent
    from PIL import Image

    client = genai.Client()

    # A video on 'The ABCs of agent building'
    video = "https://www.youtube.com/watch?v=rjoMZyxncUI"

    interaction = client.interactions.create(
        model="gemini-nano-banana-2.1",
        input=[
            VideoContent(
                uri=video,
                mime_type="video/mp4",
            ),
            TextContent(text="Generate an infographic of the topics covered in this video."),
        ],
        response_format=ImageResponseFormat(),
    )

    if interaction.output_text:
        print(interaction.output_text)

    if interaction.output_image:
        image = Image.open(BytesIO(base64.b64decode(interaction.output_image.data)))
        image.save("output_folder/video-image.png")

    # [END googlegenaisdk_interactions_imggen_mmflash_img_with_vid]
    return "output_folder/video-image.png"


if __name__ == "__main__":
    generate_content()
