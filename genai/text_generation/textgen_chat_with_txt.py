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
    # [START googlegenaisdk_textgen_chat_with_txt]
    from google import genai
    from google.genai.types import Content, Part

    client = genai.Client()
    chat = client.chats.create(
        model="gemini-2.0-flash-001",
        history=[
            Content(parts=[Part(text="Hello")], role="user"),
            Content(
                parts=[Part(text="Great to meet you. What would you like to know?")],
                role="model",
            ),
        ],
    )
    response = chat.send_message("tell me a story")
    print(response.text)
    # Example response:
    # Okay, here's a story for you:
    # ...
    # [END googlegenaisdk_textgen_chat_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
