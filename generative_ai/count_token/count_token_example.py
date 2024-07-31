# Copyright 2023 Google LLC
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
LOCATION = "us-central1"


def count_token_locally() -> int:
    # [START generativeaionvertexai_token_count_sample_with_local_sdk]
    from vertexai.preview.tokenization import get_tokenizer_for_model

    # using local tokenzier
    tokenizer = get_tokenizer_for_model("gemini-1.5-flash")

    prompt = "hello world"
    response = tokenizer.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")

    prompt = ["hello world", "what's the weather today"]
    response = tokenizer.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    # [END generativeaionvertexai_token_count_sample_with_local_sdk]
    return response.total_tokens


def count_token_service() -> int:
    # [START generativeaionvertexai_token_count_sample_with_genai]
    import vertexai
    from vertexai.generative_models import GenerativeModel

    # TODO(developer): Update project & location
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # using Vertex AI Model as tokenzier
    model = GenerativeModel("gemini-1.5-flash")

    prompt = "hello world"
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")

    prompt = ["hello world", "what's the weather today"]
    response = model.count_tokens(prompt)
    print(f"Prompt Token Count: {response.total_tokens}")
    print(f"Prompt Character Count: {response.total_billable_characters}")
    # [END generativeaionvertexai_token_count_sample_with_genai]
    return response.total_tokens


if __name__ == "__main__":
    count_token_locally()
    count_token_service()
