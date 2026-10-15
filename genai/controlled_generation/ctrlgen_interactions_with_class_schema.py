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


def create_interaction() -> str:
    # [START googlegenaisdk_interactions_ctrlgen_with_class_schema]
    import json
    from google import genai
    from google.genai.interactions import TextResponseFormat
    from pydantic import BaseModel

    class Recipe(BaseModel):
        recipe_name: str
        ingredients: list[str]

    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="List a few popular cookie recipes.",
        response_format=TextResponseFormat(
            mime_type="application/json",
            schema={
                "type": "array",
                "items": Recipe.model_json_schema(),
            },
        ),
    )

    # Use the response as a JSON string
    print(interaction.output_text)
    # Parse the response JSON into Pydantic models
    recipes = [Recipe(**r) for r in json.loads(interaction.output_text)]
    print(recipes)
    # [END googlegenaisdk_interactions_ctrlgen_with_class_schema]
    return interaction.output_text


if __name__ == "__main__":
    create_interaction()
