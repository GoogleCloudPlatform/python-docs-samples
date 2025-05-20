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


def generate_content() -> str:
    # [START googlegenaisdk_textgen_sys_instr_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents="Why is the sky blue?",
        config=GenerateContentConfig(
            system_instruction=[
                "You're a language translator.",
                "Your mission is to translate text in English to French.",
            ]
        ),
    )
    print(response.text)
    # Example response:
    # Pourquoi le ciel est-il bleu ?
    # [END googlegenaisdk_textgen_sys_instr_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
