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
    # [START googlegenaisdk_textgen_config_with_txt]
    from google import genai
    from google.genai import types

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is the sky blue?",
        # See the documentation: https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentConfig
        config=types.GenerateContentConfig(
            temperature=0,
            candidate_count=1,
            response_mime_type="application/json"
        )
    )
    print(response.text)
    # Example response:
    # {
    #   "explanation": "The sky appears blue due to a phenomenon called Rayleigh scattering. When ...
    # }
    # [END googlegenaisdk_textgen_config_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
