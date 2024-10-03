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


def chat_text_example() -> str:
    """Demonstrates a multi-turn chat interaction with a generative model."""
    # [START generativeaionvertexai_gemini_multiturn_chat]
    import vertexai

    from vertexai.generative_models import GenerativeModel, ChatSession

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    chat = model.start_chat()

    def get_chat_response(chat: ChatSession, prompt: str) -> str:
        response = chat.send_message(prompt)
        return response.text

    prompt = "Hello."
    print(get_chat_response(chat, prompt))

    prompt = "What are all the colors in a rainbow?"
    print(get_chat_response(chat, prompt))

    prompt = "Why does it appear when it rains?"
    print(get_chat_response(chat, prompt))
    # [END generativeaionvertexai_gemini_multiturn_chat]
    return get_chat_response(chat, "Hello")


def chat_stream_example() -> str:
    """Demonstrates a multi-turn chat interaction with a generative model using streaming responses"""
    # [START generativeaionvertexai_gemini_multiturn_chat_stream]
    import vertexai

    from vertexai.generative_models import GenerativeModel, ChatSession

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    chat = model.start_chat()

    def get_chat_response(chat: ChatSession, prompt: str) -> str:
        text_response = []
        responses = chat.send_message(prompt, stream=True)
        for chunk in responses:
            text_response.append(chunk.text)
        return "".join(text_response)

    prompt = "Hello."
    print(get_chat_response(chat, prompt))

    prompt = "What are all the colors in a rainbow?"
    print(get_chat_response(chat, prompt))

    prompt = "Why does it appear when it rains?"
    print(get_chat_response(chat, prompt))
    # [END generativeaionvertexai_gemini_multiturn_chat_stream]
    return get_chat_response(chat, "Hello")
