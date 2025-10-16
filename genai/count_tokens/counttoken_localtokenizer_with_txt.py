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


def counttoken_localtokenizer_with_txt() -> int:
    # [START googlegenaisdk_counttoken_localtokenizer_with_txt]
    from google.genai.local_tokenizer import LocalTokenizer

    tokenizer = LocalTokenizer(model_name="gemini-2.5-flash")
    response = tokenizer.count_tokens("What's the highest mountain in Africa?")
    print(response)
    # Example output:
    #   total_tokens=10
    # [END googlegenaisdk_counttoken_localtokenizer_with_txt]
    return response.total_tokens


if __name__ == "__main__":
    counttoken_localtokenizer_with_txt()
