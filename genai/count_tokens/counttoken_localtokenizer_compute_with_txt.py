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


def counttoken_localtokenizer_compute_with_txt() -> int:
    # [START googlegenaisdk_counttoken_localtokenizer_compute_with_txt]
    from google.genai.local_tokenizer import LocalTokenizer

    tokenizer = LocalTokenizer(model_name="gemini-2.5-flash")
    response = tokenizer.compute_tokens("What's the longest word in the English language?")
    print(response)
    # Example output:
    # tokens_info=[TokensInfo(
    #     role='user',
    #     token_ids=[3689, 236789, 236751, 506,
    #               27801, 3658, 528, 506, 5422, 5192, 236881],
    #     tokens=[b'What', b"'", b's', b' the', b' longest',
    #            b' word', b' in', b' the', b' English', b' language', b'?']
    #     )]
    # [END googlegenaisdk_counttoken_localtokenizer_compute_with_txt]
    return response.tokens_info


if __name__ == "__main__":
    counttoken_localtokenizer_compute_with_txt()
