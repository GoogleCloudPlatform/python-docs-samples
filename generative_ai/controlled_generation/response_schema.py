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


def generate_content(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id, location="us-central1")

    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "recipe_name": {
                    "type": "string",
                },
            },
            "required": ["recipe_name"],
        },
    }

    model = GenerativeModel("gemini-1.5-pro-001")

    response = model.generate_content(
        "List a few popular cookie recipes",
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_controlled_generation_response_schema]

    return response.text


def generate_content2(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_2]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id, location="us-central1")

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

    model = GenerativeModel("gemini-1.5-pro-001")

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_2]

    return response.text


def generate_content3(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_3]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id, location="us-central1")

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "forecast": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "Day": {"type": "STRING"},
                        "Forecast": {"type": "STRING"},
                        "Humidity": {"type": "STRING"},
                        "Temperature": {"type": "INTEGER"},
                        "Wind Speed": {"type": "INTEGER"},
                    },
                    "required": ["Day", "Temperature", "Forecast"],
                },
            }
        },
    }

    prompt = """
        The week ahead brings a mix of weather conditions.
        Sunday is expected to be sunny with a temperature of 77°F and a humidity level of 50%. Winds will be light at around 10 km/h.
        Monday will see partly cloudy skies with a slightly cooler temperature of 72°F and humidity increasing to 55%. Winds will pick up slightly to around 15 km/h.
        Tuesday brings rain showers, with temperatures dropping to 64°F and humidity rising to 70%. Expect stronger winds at 20 km/h.
        Wednesday may see thunderstorms, with a temperature of 68°F and high humidity of 75%. Winds will be gusty at 25 km/h.
        Thursday will be cloudy with a temperature of 66°F and moderate humidity at 60%. Winds will ease slightly to 18 km/h.
        Friday returns to partly cloudy conditions, with a temperature of 73°F and lower humidity at 45%. Winds will be light at 12 km/h.
        Finally, Saturday rounds off the week with sunny skies, a temperature of 80°F, and a humidity level of 40%. Winds will be gentle at 8 km/h.
    """

    model = GenerativeModel("gemini-1.5-pro-001")

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_3]

    return response.text


def generate_content4(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_4]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id, location="us-central1")

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

    model = GenerativeModel("gemini-1.5-pro-001")

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_4]

    return response.text


def generate_content6(project_id: str) -> str:
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_6]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel, Part

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id, location="us-central1")

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

    model = GenerativeModel("gemini-1.5-pro-001")

    response = model.generate_content(
        [
            Part.from_uri(
                "gs://cloud-samples-data/generative-ai/image/office-desk.jpeg",
                "image/jpeg",
            ),
            Part.from_uri(
                "gs://cloud-samples-data/generative-ai/image/gardening-tools.jpeg",
                "image/jpeg",
            ),
            "Generate a list of objects in the images.",
        ],
        generation_config=GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_6]

    return response.text
