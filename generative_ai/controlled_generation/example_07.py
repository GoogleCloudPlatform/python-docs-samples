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
    # [START generativeaionvertexai_gemini_controlled_generation_response_schema_7]
    import vertexai

    from vertexai.generative_models import GenerationConfig, GenerativeModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-pro")

    response_schema = {"type": "STRING", "enum": ["drama", "comedy", "documentary"]}

    prompt = (
        "The film aims to educate and inform viewers about real-life subjects, events, or people."
        "It offers a factual record of a particular topic by combining interviews, historical footage, "
        "and narration. The primary purpose of a film is to present information and provide insights "
        "into various aspects of reality."
    )

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="text/x.enum", response_schema=response_schema
        ),
    )

    print(response.text)
    # Example response:
    #     'documentary'

    # [END generativeaionvertexai_gemini_controlled_generation_response_schema_7]
    return response.text


if __name__ == "__main__":
    generate_content()
