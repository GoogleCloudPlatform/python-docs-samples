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
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_4]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "to_discard": {"type": "INTEGER"},
                "subcategory": {"type": "STRING"},
                "safe_handling": {"type": "INTEGER"},
                "item_category": {
                    "type": "STRING",
                    "enum": [
                        "clothing",
                        "winter apparel",
                        "specialized apparel",
                        "furniture",
                        "decor",
                        "tableware",
                        "cookware",
                        "toys",
                    ],
                },
                "for_resale": {"type": "INTEGER"},
                "condition": {
                    "type": "STRING",
                    "enum": [
                        "new in package",
                        "like new",
                        "gently used",
                        "used",
                        "damaged",
                        "soiled",
                    ],
                },
            },
        },
    }

    prompt = """
        Item description:
        The item is a long winter coat that has many tears all around the seams and is falling apart.
        It has large questionable stains on it.
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
    #     {
    #         "condition": "damaged",
    #         "item_category": "clothing",
    #         "subcategory": "winter apparel",
    #         "to_discard": 123,
    #     }
    # ]

    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_4]
    return response.text


if __name__ == "__main__":
    generate_content()
