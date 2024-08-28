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


def generate_from_text_input() -> str:
    # [START generativeaionvertexai_gemini_generate_from_text_input]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update project_id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-001")

    response = model.generate_content(
        "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
    )

    print(response.text)
    # [END generativeaionvertexai_gemini_generate_from_text_input]

    return response.text


if __name__ == "__main__":
    generate_from_text_input()
