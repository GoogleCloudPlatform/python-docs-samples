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
    from google.genai.types import GenerateContentConfig, HttpOptions, Part, SafetySetting

    from PIL import Image, ImageColor, ImageDraw

    from pydantic import BaseModel

    # Helper class to represent a bounding box
    class BoundingBox(BaseModel):
        """
        Represents a bounding box with its 2D coordinates and associated label.

        Attributes:
            box_2d (list[int]): A list of integers representing the 2D coordinates of the bounding box,
                                typically in the format [x_min, y_min, x_max, y_max].
            label (str): A string representing the label or class associated with the object within the bounding box.
        """

        box_2d: list[int]
        label: str

    # Helper function to plot bounding boxes on an image
    def plot_bounding_boxes(image_uri: str, bounding_boxes: list[BoundingBox]) -> None:
        """
        Plots bounding boxes on an image with markers for each a name, using PIL, normalized coordinates, and different colors.

        Args:
            img_path: The path to the image file.
            bounding_boxes: A list of bounding boxes containing the name of the object
            and their positions in normalized [y1 x1 y2 x2] format.
        """
        with Image.open(requests.get(image_uri, stream=True, timeout=10).raw) as im:
            width, height = im.size
            draw = ImageDraw.Draw(im)

            colors = list(ImageColor.colormap.keys())

            for i, bbox in enumerate(bounding_boxes):
                y1, x1, y2, x2 = bbox.box_2d
                abs_y1 = int(y1 / 1000 * height)
                abs_x1 = int(x1 / 1000 * width)
                abs_y2 = int(y2 / 1000 * height)
                abs_x2 = int(x2 / 1000 * width)

                color = colors[i % len(colors)]

                draw.rectangle(
                    ((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=4
                )
                if bbox.label:
                    draw.text((abs_x1 + 8, abs_y1 + 6), bbox.label, fill=color)

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
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            ),
        ],
        response_mime_type="application/json",
        response_schema=list[BoundingBox],  # Add BoundingBox class to the response schema
    )

    image_uri = "https://storage.googleapis.com/generativeai-downloads/images/socks.jpg"

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
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
    #     {"box_2d": [36, 246, 380, 492], "label": "top left sock with face"},
    #     {"box_2d": [260, 663, 640, 917], "label": "top right sock with face"},
    # ]
    # [END googlegenaisdk_boundingbox_with_txt_img]
    return response.text


if __name__ == "__main__":
    generate_content()
