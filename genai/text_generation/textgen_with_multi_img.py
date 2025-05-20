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
    # [START googlegenaisdk_textgen_with_multi_img]
    from google import genai
    from google.genai.types import HttpOptions, Part

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Read content from GCS
    gcs_file_img_path = "gs://cloud-samples-data/generative-ai/image/scones.jpg"

    # Read content from a local file
    with open("test_data/latte.jpg", "rb") as f:
        local_file_img_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[
            "Generate a list of all the objects contained in both images.",
            Part.from_uri(file_uri=gcs_file_img_path, mime_type="image/jpeg"),
            Part.from_bytes(data=local_file_img_bytes, mime_type="image/jpeg"),
        ],
    )
    print(response.text)
    # Example response:
    # Okay, here's the list of objects present in both images:
    # ...
    # [END googlegenaisdk_textgen_with_multi_img]
    return response.text


if __name__ == "__main__":
    generate_content()
