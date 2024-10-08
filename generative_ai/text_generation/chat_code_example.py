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


def write_a_function() -> object:
    """Example of using Codey for Code Chat Model to write a function."""
    # [START generativeaionvertexai_sdk_code_chat]
    from vertexai.language_models import CodeChatModel

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": 0.5,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat_session = code_chat_model.start_chat()

    response = chat_session.send_message(
        "Please help write a function to calculate the min of two numbers", **parameters
    )
    print(f"Response from Model: {response.text}")
    # Response from Model: Sure, here is a function that you can use to calculate the minimum of two numbers:
    # ```
    # def min(a, b):
    #   """
    #   Calculates the minimum of two numbers.
    #   Args:
    #     a: The first number.
    # ...

    # [END generativeaionvertexai_sdk_code_chat]
    return response


if __name__ == "__main__":
    write_a_function()
