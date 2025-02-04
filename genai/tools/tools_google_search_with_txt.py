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
    from google import genai
    from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="When is the next total solar eclipse in the United States?",
        config=GenerateContentConfig(
            tools=[
                # Use Google Search Tool
                Tool(google_search=GoogleSearch())
            ],
        ),
    )

    print(response.candidates[0].content.parts[0].text)
    # Example response:
    # 'The next total solar eclipse in the United States will occur on ...'
    return response.candidates[0].content.parts[0].text


if __name__ == "__main__":
    generate_content()
