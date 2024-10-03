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

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def set_system_instruction() -> str:
    # [START generativeaionvertexai_gemini_system_instruction]
    import vertexai

    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel(
        model_name="gemini-1.5-flash-002",
        system_instruction=[
            "You are a helpful language translator.",
            "Your mission is to translate text in English to French.",
        ],
    )

    prompt = """
    User input: I like bagels.
    Answer:
    """
    response = model.generate_content([prompt])
    print(response.text)
    # Example response:
    # J'aime les bagels.

    # [END generativeaionvertexai_gemini_system_instruction]
    return response.text


if __name__ == "__main__":
    set_system_instruction()
