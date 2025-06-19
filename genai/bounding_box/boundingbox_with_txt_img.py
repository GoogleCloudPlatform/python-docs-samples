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
    # [START googlegenaisdk_boundingbox_with_txt_img]
    import requests
    from google import genai
    from google.genai.types import (
        GenerateContentConfig,
        HarmBlockThreshold,
        HarmCategory,
        HttpOptions,
        Part,
        SafetySetting,
    )
    from PIL import Image, ImageColor, ImageDraw
    from pydantic import BaseModel

    # Helper class to represent a bounding box
    class BoundingBox(BaseModel):
        """
        Represents a bounding box with its 2D coordinates and associated label.

        Attributes:
            box_2d (list[int]): A list of integers representing the 2D coordinates of the bounding box,
                                typically in the format [y_min, x_min, y_max, x_max].
            label (str): A string representing the label or class associated with the object within the bounding box.
        """

        box_2d: list[int]
        label: str

    # Helper function to plot bounding boxes on an image
    def plot_bounding_boxes(image_uri: str, bounding_boxes: list[BoundingBox]) -> None:
        """
        Plots bounding boxes on an image with labels, using PIL and normalized coordinates.

        Args:
            image_uri: The URI of the image file.
            bounding_boxes: A list of BoundingBox objects. Each box's coordinates are in
                            normalized [y_min, x_min, y_max, x_max] format.
        """
        with Image.open(requests.get(image_uri, stream=True, timeout=10).raw) as im:
            width, height = im.size
            draw = ImageDraw.Draw(im)

            colors = list(ImageColor.colormap.keys())

            for i, bbox in enumerate(bounding_boxes):
                # Scale normalized coordinates to image dimensions
                abs_y_min = int(bbox.box_2d[0] / 1000 * height)
                abs_x_min = int(bbox.box_2d[1] / 1000 * width)
                abs_y_max = int(bbox.box_2d[2] / 1000 * height)
                abs_x_max = int(bbox.box_2d[3] / 1000 * width)

                color = colors[i % len(colors)]

                # Draw the rectangle using the correct (x, y) pairs
                draw.rectangle(
                    ((abs_x_min, abs_y_min), (abs_x_max, abs_y_max)),
                    outline=color,
                    width=4,
                )
                if bbox.label:
                    # Position the text at the top-left corner of the box
                    draw.text((abs_x_min + 8, abs_y_min + 6), bbox.label, fill=color)

            im.show()

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    config = GenerateContentConfig(
        system_instruction="""
        Return bounding boxes as an array with labels.
        Never return masks. Limit to 25 objects.
        If an object is present multiple times, give each object a unique label
        according to its distinct characteristics (colors, size, position, etc..).
        """,
        temperature=0.5,
        safety_settings=[
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
            ),
        ],
        response_mime_type="application/json",
        response_schema=list[BoundingBox],
    )

    image_uri = "https://storage.googleapis.com/generativeai-downloads/images/socks.jpg"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            Part.from_uri(
                file_uri=image_uri,
                mime_type="image/jpeg",
            ),
            "Output the positions of the socks with a face. Label according to position in the image.",
        ],
        config=config,
    )
    print(response.text)
    plot_bounding_boxes(image_uri, response.parsed)

    # Example response:
    # [
    #     {"box_2d": [6, 246, 386, 526], "label": "top-left light blue sock with cat face"},
    #     {"box_2d": [234, 649, 650, 863], "label": "top-right light blue sock with cat face"},
    # ]
    # [END googlegenaisdk_boundingbox_with_txt_img]
    return response.text


if __name__ == "__main__":
    generate_content()
