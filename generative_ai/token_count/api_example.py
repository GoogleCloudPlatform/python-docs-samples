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


def count_token_api_example() -> int:
    # [START generativeaionvertexai_token_count_sample_with_genai]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update project & location
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # using Vertex AI Model as tokenzier
    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = "hello world"
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")
    # Example response:
    #     Prompt Token Count: 2
    #     Prompt Token Count: 10

    prompt = ["hello world", "what's the weather today"]
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")
    # Example response:
    #     Prompt Token Count: 8
    #     Prompt Token Count: 31
    # [END generativeaionvertexai_token_count_sample_with_genai]
    return response.total_tokens


if __name__ == "__main__":
    count_token_api_example()
