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


def send_chat() -> str:
    # [START generativeaionvertexai_chat]
    from vertexai.language_models import ChatModel, InputOutputTextPair

    chat_model = ChatModel.from_pretrained("chat-bison@002")

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }

    chat_session = chat_model.start_chat(
        context="My name is Miles. You are an astronomer, knowledgeable about the solar system.",
        examples=[
            InputOutputTextPair(
                input_text="How many moons does Mars have?",
                output_text="The planet Mars has two moons, Phobos and Deimos.",
            ),
        ],
    )

    response = chat_session.send_message(
        "How many planets are there in the solar system?", **parameters
    )
    print(response.text)
    # Example response:
    # There are eight planets in the solar system:
    # Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.

    # [END generativeaionvertexai_chat]
    return response.text


if __name__ == "__main__":
    send_chat()
