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
    # [START googlegenaisdk_ctrlgen_with_class_schema]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

    from pydantic import BaseModel

    class Recipe(BaseModel):
        recipe_name: str
        ingredients: list[str]

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents="List a few popular cookie recipes.",
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[Recipe],
        ),
    )
    # Use the response as a JSON string.
    print(response.text)
    # Use the response as an object
    print(response.parsed)

    # Example output:
    # [Recipe(recipe_name='Chocolate Chip Cookies', ingredients=['2 1/4 cups all-purpose flour'
    #   {
    #     "ingredients": [
    #       "2 1/4 cups all-purpose flour",
    #       "1 teaspoon baking soda",
    #       "1 teaspoon salt",
    #       "1 cup (2 sticks) unsalted butter, softened",
    #       "3/4 cup granulated sugar",
    #       "3/4 cup packed brown sugar",
    #       "1 teaspoon vanilla extract",
    #       "2 large eggs",
    #       "2 cups chocolate chips"
    #     ],
    #     "recipe_name": "Classic Chocolate Chip Cookies"
    #   }, ... ]
    # [END googlegenaisdk_ctrlgen_with_class_schema]
    return response.text


if __name__ == "__main__":
    generate_content()
