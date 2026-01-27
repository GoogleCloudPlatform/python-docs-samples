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
    # [START googlegenaisdk_codeexecution_with_txt_tableimg]
    import io
    from PIL import Image
    from google import genai
    from google.genai import types

    # Read a local image as input
    image_pil = Image.open("sample_images/tabular_data.png")
    image_pil = image_pil.convert("RGB")
    byte_io = io.BytesIO()
    image_pil.save(byte_io, format="JPEG")
    image_bytes = byte_io.getvalue()
    image = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            image,
            "Make a bar chart of per-category performance, normalize prior SOTA as 1.0 for each task,"
            "then take average per-category. Plot using matplotlib with nice style.",
        ],
        config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution)]),
    )

    img_count = 0
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        if part.executable_code is not None:
            print("####################### 1. Generate Python Code #######################")
            print(part.executable_code.code)
        if part.code_execution_result is not None:
            print("####################### 2. Executing Python Code #######################")
            print(part.code_execution_result.output)
        # For local executions, save the output to a local filename
        if part.as_image() is not None:
            print("####################### 3. Save Output #######################")
            img_count += 1
            output_location = f"sample_images/output-barplot-{img_count}.jpg"
            image_data = part.as_image().image_bytes
            image = Image.open(io.BytesIO(image_data))
            image = image.convert("RGB")
            image.save(output_location)
            print(f"Output is saved to {output_location}")
    # Example response:
    #
    # [END googlegenaisdk_codeexecution_with_txt_tableimg]
    return True


if __name__ == "__main__":
    generate_content()
