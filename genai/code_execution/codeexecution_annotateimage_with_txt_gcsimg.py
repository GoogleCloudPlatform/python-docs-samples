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
    # [START googlegenaisdk_codeexecution_annotateimage_with_txt_gcsimg]
    import io
    from PIL import Image
    from google import genai
    from google.genai import types


    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Part.from_uri(
                file_uri="https://storage.googleapis.com/cloud-samples-data/generative-ai/image/robotic.jpeg",
                mime_type="image/png",
            ),
            "Annotate on the image with arrows of different colors, which object should go into which bin.",
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
            output_location = f"sample_images/output-annotate-image-{img_count}.jpg"
            image_data = part.as_image().image_bytes
            image = Image.open(io.BytesIO(image_data))
            image = image.convert("RGB")
            image.save(output_location)
            print(f"Output is saved to {output_location}")
    # Example response:
    #     ####################### 1. Generate Python Code #######################
    #     import PIL.Image
    #     import PIL.ImageDraw
    #
    #     # Load the image to get dimensions
    #     img = PIL.Image.open('f_https___storage.googleapis.com_cloud_samples_data_generative_ai_image_robotic.jpeg')
    #     width, height = img.size
    #
    #     # Define objects and bins with normalized coordinates [ymin, xmin, ymax, xmax]
    #     bins = {
    #         'light_blue': [118, 308, 338, 436],
    #         'green': [248, 678, 458, 831],
    #         'black': [645, 407, 898, 578]
    #     }
    #
    #     objects = [
    #         {'name': 'green pepper', 'box': [256, 482, 296, 546], 'target': 'green'},
    #         {'name': 'red pepper', 'box': [317, 478, 349, 544], 'target': 'green'},
    #         {'name': 'grapes', 'box': [584, 555, 664, 593], 'target': 'green'},
    #         {'name': 'cherries', 'box': [463, 671, 511, 718], 'target': 'green'},
    #         {'name': 'soda can', 'box': [397, 524, 489, 605], 'target': 'light_blue'},
    #         {'name': 'brown snack', 'box': [397, 422, 475, 503], 'target': 'black'},
    #         {'name': 'welch snack', 'box': [520, 466, 600, 543], 'target': 'black'},
    #         {'name': 'paper towel', 'box': [179, 564, 250, 607], 'target': 'black'},
    #         {'name': 'plastic cup', 'box': [271, 587, 346, 643], 'target': 'black'},
    #     ]
    #
    #     # Helper to get center of a normalized box
    #     def get_center(box):
    #         ymin, xmin, ymax, xmax = box
    #         return ((xmin + xmax) / 2000 * width, (ymin + ymax) / 2000 * height)
    #
    #     draw = PIL.ImageDraw.Draw(img)
    #
    #     # Define arrow colors based on target bin
    #     colors = {
    #         'green': 'green',
    #         'light_blue': 'blue',
    #         'black': 'red'
    #     }
    #
    #     for obj in objects:
    #         start_point = get_center(obj['box'])
    #         end_point = get_center(bins[obj['target']])
    #         color = colors[obj['target']]
    #         # Drawing a line with an arrow head (simulated with a few extra lines)
    #         draw.line([start_point, end_point], fill=color, width=5)
    #         # Simple arrowhead
    #         import math
    #         angle = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
    #         arrow_len = 20
    #         p1 = (end_point[0] - arrow_len * math.cos(angle - math.pi / 6),
    #               end_point[1] - arrow_len * math.sin(angle - math.pi / 6))
    #         p2 = (end_point[0] - arrow_len * math.cos(angle + math.pi / 6),
    #               end_point[1] - arrow_len * math.sin(angle + math.pi / 6))
    #         draw.line([end_point, p1], fill=color, width=5)
    #         draw.line([end_point, p2], fill=color, width=5)
    #
    #     img.save('annotated_robotic.jpeg')
    #
    #     # Also list detections for confirmation
    #     # [
    #     #   {"box_2d": [118, 308, 338, 436], "label": "light blue bin"},
    #     #   {"box_2d": [248, 678, 458, 831], "label": "green bin"},
    #     #   {"box_2d": [645, 407, 898, 578], "label": "black bin"},
    #     #   {"box_2d": [256, 482, 296, 546], "label": "green pepper"},
    #     #   {"box_2d": [317, 478, 349, 544], "label": "red pepper"},
    #     #   {"box_2d": [584, 555, 664, 593], "label": "grapes"},
    #     #   {"box_2d": [463, 671, 511, 718], "label": "cherries"},
    #     #   {"box_2d": [397, 524, 489, 605], "label": "soda can"},
    #     #   {"box_2d": [397, 422, 475, 503], "label": "brown snack"},
    #     #   {"box_2d": [520, 466, 600, 543], "label": "welch snack"},
    #     #   {"box_2d": [179, 564, 250, 607], "label": "paper towel"},
    #     #   {"box_2d": [271, 587, 346, 643], "label": "plastic cup"}
    #     # ]
    #
    #     ####################### 2. Executing Python Code #######################
    #     None
    #     ####################### 3. Save Output #######################
    #     Output is saved to sample_images/output-annotate-image-1.jpg
    #     The image has been annotated with arrows indicating the appropriate bin for each object based on standard waste sorting practices:
    #
    #     - **Green Arrows (Compost):** Organic items such as the green pepper, red pepper, grapes, and cherries are directed to the **green bin**.
    #     - **Blue Arrow (Recycling):** The crushed soda can is directed to the **light blue bin**.
    #     - **Red Arrows (Trash/Landfill):** Non-recyclable or contaminated items like the snack wrappers (brown and Welch's), the white paper towel, and the small plastic cup are directed to the **black bin**.
    #
    #     These categorizations follow common sorting rules where green is for organics, blue for recyclables, and black for general waste.
    # [END googlegenaisdk_codeexecution_annotateimage_with_txt_gcsimg]
    return True


if __name__ == "__main__":
    generate_content()
