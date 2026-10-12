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
    # [START googlegenaisdk_interactions_ctrlgen_with_resp_schema]
    from google import genai

    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "recipe_name": {"type": "string"},
                "ingredients": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["recipe_name", "ingredients"],
        },
    }

    prompt = """
        List a few popular cookie recipes.
    """

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": response_schema,
        },
    )

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_ctrlgen_with_resp_schema]
    return interaction.output_text


if __name__ == "__main__":
    generate_content()
