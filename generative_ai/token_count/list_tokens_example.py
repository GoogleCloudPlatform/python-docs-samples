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


def list_tokens_example() -> int:
    # [START generativeaionvertexai_compute_tokens]
    from vertexai.preview.tokenization import get_tokenizer_for_model

    # init local tokenzier
    tokenizer = get_tokenizer_for_model("gemini-1.5-flash-001")

    # Count Tokens
    prompt = "why is the sky blue?"
    response = tokenizer.count_tokens(prompt)
    print(f"Tokens count: {response.total_tokens}")
    # Example response:
    #       Tokens count: 6

    # Compute Tokens
    response = tokenizer.compute_tokens(prompt)
    print(f"Tokens list: {response.tokens_info}")
    # Example response:
    #     Tokens list: [TokensInfo(token_ids=[18177, 603, 573, 8203, 3868, 235336],
    #          tokens=[b'why', b' is', b' the', b' sky', b' blue', b'?'], role='user')]
    # [END generativeaionvertexai_compute_tokens]
    return len(response.tokens_info)


if __name__ == "__main__":
    list_tokens_example()
