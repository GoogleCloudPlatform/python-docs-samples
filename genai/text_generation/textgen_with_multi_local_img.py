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


def generate_content(image_path_1: str, image_path_2: str) -> str:
    # [START googlegenaisdk_textgen_with_multi_local_img]
    from google import genai
    from google.genai.types import HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    # TODO(Developer): Update the below file paths to your images
    # image_path_1 = "path/to/your/image1.jpg"
    # image_path_2 = "path/to/your/image2.jpg"
    with open(image_path_1, "rb") as f:
        image_1_bytes = f.read()
    with open(image_path_2, "rb") as f:
        image_2_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[
            "Generate a list of all the objects contained in both images.",
            Part.from_bytes(data=image_1_bytes, mime_type="image/jpeg"),
            Part.from_bytes(data=image_2_bytes, mime_type="image/jpeg"),
        ],
    )
    print(response.text)
    # Example response:
    # Okay, here's a jingle combining the elements of both sets of images, focusing on ...
    # ...
    # [END googlegenaisdk_textgen_with_multi_local_img]
    return response.text


if __name__ == "__main__":
    generate_content(
        "./test_data/latte.jpg",
        "./test_data/scones.jpg",
    )
