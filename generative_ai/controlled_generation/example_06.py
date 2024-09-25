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
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_6]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "object": {"type": "STRING"},
                },
            },
        },
    }

    model = GenerativeModel("gemini-1.5-pro-002")

    response = model.generate_content(
        [
            # Text prompt
            "Generate a list of objects in the images.",
            # Http Image
            Part.from_uri(
                "https://storage.googleapis.com/cloud-samples-data/generative-ai/image/office-desk.jpeg",
                "image/jpeg",
            ),
            # Cloud storage object
            Part.from_uri(
                "gs://cloud-samples-data/generative-ai/image/gardening-tools.jpeg",
                "image/jpeg",
            ),
        ],
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # Example response:
    # [
    #     [
    #         {"object": "globe"}, {"object": "tablet"}, {"object": "toy car"},
    #         {"object": "airplane"}, {"object": "keyboard"}, {"object": "mouse"},
    #         {"object": "passport"}, {"object": "sunglasses"}, {"object": "money"},
    #         {"object": "notebook"}, {"object": "pen"}, {"object": "coffee cup"},
    #     ],
    #     [
    #         {"object": "watering can"}, {"object": "plant"}, {"object": "flower pot"},
    #         {"object": "gloves"}, {"object": "garden tool"},
    #     ],
    # ]

    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_6]
    return response.text


if __name__ == "__main__":
    generate_content()
