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
    # [START googlegenaisdk_ctrlgen_with_enum_schema]
    from google import genai

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="What type of instrument is an oboe?",
        config={
            "response_mime_type": "text/x.enum",
            "response_schema": {
                "type": "STRING",
                "enum": ["Percussion", "String", "Woodwind", "Brass", "Keyboard"],
            },
        },
    )

    print(response.text)
    # Example output:
    # Woodwind

    # [END googlegenaisdk_ctrlgen_with_enum_schema]
    return response.text


if __name__ == "__main__":
    generate_content()
