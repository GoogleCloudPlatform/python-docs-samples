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
    # [START googlegenaisdk_codeexecution_with_txt_img]
    import io
    from PIL import Image
    from google import genai
    from google.genai import types

    # Read a local image as input
    image_pil = Image.open("sample_images/instrument-img.jpg")
    byte_io = io.BytesIO()
    image_pil.save(byte_io, format="JPEG")
    image_bytes = byte_io.getvalue()
    image = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            image,
            "Zoom into the expression pedals and tell me how many pedals are there?",
        ],
        config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution)]),
    )

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
            image_data = part.as_image().image_bytes
            image = Image.open(io.BytesIO(image_data))
            output_location = "sample_images/instrument-img-output.jpg"
            image.save(output_location)
            print(f"Output is saved to {output_location}")
    # Example response:
    #     ####################### 1. Generate Python Code #######################
    #     import PIL.Image
    #     import PIL.ImageDraw
    #
    #     # Load the image to get its dimensions
    #     img = PIL.Image.open('input_file_0.jpeg')
    #     width, height = img.size
    #
    #     # Define the region for expression pedals
    #     # Expression pedals are in the middle, roughly around y=450 to 600, x=450 to 650 (normalized)
    #     # Let's refine based on the image
    #     # Actually, they are between roughly 45% and 60% of width, and 45% to 60% of height.
    #     expression_pedals_bbox = [463, 467, 606, 608] # [ymin, xmin, ymax, xmax] in normalized coordinates
    #
    #     # Convert normalized to pixel coordinates
    #     def norm_to_pixel(norm_bbox, w, h):
    #         ymin, xmin, ymax, xmax = norm_bbox
    #         return [int(ymin * h / 1000), int(xmin * w / 1000), int(ymax * h / 1000), int(xmax * w / 1000)]
    #
    #     pixel_bbox = norm_to_pixel(expression_pedals_bbox, width, height)
    #
    #     # Crop and save
    #     crop = img.crop((pixel_bbox[1], pixel_bbox[0], pixel_bbox[3], pixel_bbox[2]))
    #     crop.save('expression_pedals_zoom.png')
    #
    #     # Output detection for internal reference
    #     print(f'# [{{box_2d: {expression_pedals_bbox}, label: "expression pedals"}}]')
    #
    #     ####################### 2. Executing Python Code #######################
    #     # [{box_2d: [463, 467, 606, 608], label: "expression pedals"}]
    #
    #     ####################### 3. Save Output #######################
    #     Output is saved to sample_images/instrument-img-output.jpg
    #     Based on the zoomed-in image, there are 4 expression pedals located in the center of the organ console, just above the pedalboard.
    # [END googlegenaisdk_codeexecution_with_txt_img]
    return True


if __name__ == "__main__":
    generate_content()
