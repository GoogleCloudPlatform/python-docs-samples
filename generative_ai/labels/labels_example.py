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

from vertexai.generative_models import GenerationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_content() -> GenerationResponse:
    # [START generativeaionvertexai_gemini_set_labels]
    import vertexai

    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-2.0-flash-001")

    prompt = "What is Generative AI?"
    response = model.generate_content(
        prompt,
        # Example Labels
        labels={
            "team": "research",
            "component": "frontend",
            "environment": "production",
        },
    )

    print(response.text)
    # Example response:
    # Generative AI is a type of Artificial Intelligence focused on **creating new content** based on existing data.

    # [END generativeaionvertexai_gemini_set_labels]
    return response


if __name__ == "__main__":
    generate_content()
