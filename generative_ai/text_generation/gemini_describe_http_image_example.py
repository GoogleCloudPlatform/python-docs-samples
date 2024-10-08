# Copyright 2024 Google LLC
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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_content() -> str:
    # [START generativeaionvertexai_gemini_describe_http_image]
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    # TODO (developer): update project id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    contents = [
        # Text prompt
        "Describe this image.",
        # Example image of a Jack Russell Terrier puppy from Wikipedia.
        Part.from_uri(
            "https://upload.wikimedia.org/wikipedia/commons/1/1d/Szczenie_Jack_Russell_Terrier.jpg",
            "image/jpeg",
        ),
    ]

    response = model.generate_content(contents)
    print(response.text)
    # Example response:
    #     'Here is a description of the image:'
    #     'Close-up view of a young Jack Russell Terrier puppy sitting in short grass ...'

    # [END generativeaionvertexai_gemini_describe_http_image]
    return response.text


if __name__ == "__main__":
    generate_content()
