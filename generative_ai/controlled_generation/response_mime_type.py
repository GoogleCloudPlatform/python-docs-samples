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
    # [START generativeaionvertexai_gemini_controlled_generation_response_mime_type]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # project_id = "PROJECT_ID"
    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    prompt = """
        List a few popular cookie recipes using this JSON schema:
        Recipe = {"recipe_name": str}
        Return: `list[Recipe]`
    """

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(response_mime_type="application/json"),
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_controlled_generation_response_mime_type]

    return response.text
