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
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_2]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

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
                    "rating": {"type": "INTEGER"},
                    "flavor": {"type": "STRING"},
                },
            },
        },
    }

    prompt = """
        Reviews from our social media:
        - "Absolutely loved it! Best ice cream I've ever had." Rating: 4, Flavor: Strawberry Cheesecake
        - "Quite good, but a bit too sweet for my taste." Rating: 1, Flavor: Mango Tango
    """

    model = GenerativeModel("gemini-1.5-pro-002")

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # Example response:
    # [
    #     [
    #         {"flavor": "Strawberry Cheesecake", "rating": 4},
    #         {"flavor": "Mango Tango", "rating": 1},
    #     ]
    # ]

    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_2]
    return response.text


if __name__ == "__main__":
    generate_content()
