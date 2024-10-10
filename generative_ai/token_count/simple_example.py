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


def count_token_example() -> GenerationResponse:
    # [START generativeaionvertexai_gemini_token_count]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = "Why is the sky blue?"
    # Prompt tokens count
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")

    # Send text to Gemini
    response = model.generate_content(prompt)

    # Response tokens count
    usage_metadata = response.usage_metadata
    print(f"Prompt Token Count: {usage_metadata.prompt_token_count}")
    print(f"Candidates Token Count: {usage_metadata.candidates_token_count}")
    print(f"Total Token Count: {usage_metadata.total_token_count}")
    # Example response:
    # Prompt Token Count: 6
    # Prompt Character Count: 16
    # Prompt Token Count: 6
    # Candidates Token Count: 315
    # Total Token Count: 321

    # [END generativeaionvertexai_gemini_token_count]
    return response


if __name__ == "__main__":
    count_token_example()
