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


def create_interaction() -> bool:
    # [START googlegenaisdk_interactions_codeexecution_cropimage_with_txt_img]
    import base64
    import io
    import requests
    from PIL import Image
    from google import genai
    from google.genai.interactions import CodeExecution, ImageContent, TextContent

    # Download the input image
    image_path = "https://storage.googleapis.com/cloud-samples-data/generative-ai/image/chips.jpeg"
    image_bytes = requests.get(image_path).content
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            ImageContent(data=b64_image, mime_type="image/jpeg"),
            TextContent(text="Locate the ESMT chip. What are the numbers on the chip?"),
        ],
        tools=[CodeExecution()],
    )

    for step in interaction.steps:
        if step.type == "code_execution_call":
            print("####################### 1. Generate Python Code #######################")
            print(step.arguments.code)
        elif step.type == "code_execution_result":
            print("####################### 2. Executing Python Code #######################")
            print(step.result)

    if interaction.output_image:
        print("####################### 3. Save Output #######################")
        image_data = base64.b64decode(interaction.output_image.data)
        image = Image.open(io.BytesIO(image_data))
        output_location = "ESMT-chip-output.jpg"
        image.save(output_location)
        print(f"Output is saved to {output_location}")

    if interaction.output_text:
        print(interaction.output_text)

    # [END googlegenaisdk_interactions_codeexecution_cropimage_with_txt_img]
    return True


if __name__ == "__main__":
    create_interaction()
