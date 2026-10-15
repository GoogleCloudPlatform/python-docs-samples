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
    # [START googlegenaisdk_interactions_codeexecution_annotateimage_with_txt_gcsimg]
    import base64
    import io
    from PIL import Image
    from google import genai
    from google.genai.interactions import CodeExecution, ImageContent, TextContent

    client = genai.Client()

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            ImageContent(
                uri="https://storage.googleapis.com/cloud-samples-data/generative-ai/image/robotic.jpeg",
                mime_type="image/jpeg",
            ),
            TextContent(
                text="Annotate on the image with arrows of different colors, which object should go into which bin."
            ),
        ],
        tools=[CodeExecution()],
    )

    img_count = 0
    for step in interaction.steps:
        if step.type == "code_execution_call":
            print("####################### 1. Generate Python Code #######################")
            print(step.arguments.code)
        elif step.type == "code_execution_result":
            print("####################### 2. Executing Python Code #######################")
            print(step.result)

    if interaction.output_image:
        print("####################### 3. Save Output #######################")
        img_count += 1
        output_location = f"robotic-annotate-output-{img_count}.jpg"
        image_bytes = base64.b64decode(interaction.output_image.data)
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image.save(output_location)
        print(f"Output is saved to {output_location}")

    if interaction.output_text:
        print(interaction.output_text)

    # [END googlegenaisdk_interactions_codeexecution_annotateimage_with_txt_gcsimg]
    return True


if __name__ == "__main__":
    create_interaction()
