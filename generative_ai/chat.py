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

# [START aiplatform_sdk_chat]
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


def science_tutoring(temperature=.2):

    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }

    chat = chat_model.start_chat(
        context="My name is Miles. You are an astronomer, knowledgeable about the solar system.",
        examples=[
            InputOutputTextPair(
                input_text='How many moons does Mars have?',
                output_text='The planet Mars has two moons, Phobos and Deimos.',
            ),
        ]
    )

    response = chat.send_message("How many planets are there in the solar system?", **parameters)
    print(f"Response from Model: {response.text}")
# [END aiplatform_sdk_chat]

    return response


if __name__ == "__main__":
    science_tutoring()
