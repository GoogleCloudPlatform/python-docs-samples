# Copyright 2023 Google LLC
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

import vertexai


def generate_text_multimodal(project_id: str, location: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # [START generativeaionvertexai_gemini_single_turn_multi_image]
    import http.client
    import typing
    import urllib.request
    from vertexai.generative_models import GenerativeModel, Image

    # create helper function
    def load_image_from_url(image_url: str) -> Image:
        with urllib.request.urlopen(image_url) as response:
            response = typing.cast(http.client.HTTPResponse, response)
            image_bytes = response.read()
        return Image.from_bytes(image_bytes)

    # Load images from Cloud Storage URI
    landmark1 = load_image_from_url(
        "https://storage.googleapis.com/cloud-samples-data/vertex-ai/llm/prompts/landmark1.png"
    )
    landmark2 = load_image_from_url(
        "https://storage.googleapis.com/cloud-samples-data/vertex-ai/llm/prompts/landmark2.png"
    )
    landmark3 = load_image_from_url(
        "https://storage.googleapis.com/cloud-samples-data/vertex-ai/llm/prompts/landmark3.png"
    )

    # Pass multimodal prompt
    model = GenerativeModel("gemini-1.0-pro-vision")
    response = model.generate_content(
        [
            landmark1,
            "city: Rome, Landmark: the Colosseum",
            landmark2,
            "city: Beijing, Landmark: Forbidden City",
            landmark3,
        ]
    )
    print(response)
    # [END generativeaionvertexai_gemini_single_turn_multi_image]
    return response.text
