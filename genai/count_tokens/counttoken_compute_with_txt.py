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


def compute_tokens_example() -> int:
    # [START googlegenaisdk_counttoken_compute_with_txt]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.compute_tokens(
        model="gemini-2.5-flash-preview-05-20",
        contents="What's the longest word in the English language?",
    )

    print(response)
    # Example output:
    # tokens_info=[TokensInfo(
    #    role='user',
    #    token_ids=[1841, 235303, 235256, 573, 32514, 2204, 575, 573, 4645, 5255, 235336],
    #    tokens=[b'What', b"'", b's', b' the', b' longest', b' word', b' in', b' the', b' English', b' language', b'?']
    #  )]
    # [END googlegenaisdk_counttoken_compute_with_txt]
    return response.tokens_info


if __name__ == "__main__":
    compute_tokens_example()
