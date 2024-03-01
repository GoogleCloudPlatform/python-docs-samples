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

# [START aiplatform_streaming_chat]
import vertexai
from vertexai import language_models


def streaming_prediction(
    project_id: str,
    location: str,
) -> str:
    """Streaming Chat Example with a Large Language Model."""

    vertexai.init(project=project_id, location=location)

    chat_model = language_models.ChatModel.from_pretrained("chat-bison")

    parameters = {
        # Temperature controls the degree of randomness in token selection.
        "temperature": 0.8,
        # Token limit determines the maximum amount of text output.
        "max_output_tokens": 256,
        # Tokens are selected from most probable to least until the
        # sum of their probabilities equals the top_p value.
        "top_p": 0.95,
        # A top_k of 1 means the selected token is the most probable among
        # all tokens.
        "top_k": 40,
    }

    chat = chat_model.start_chat(
        context="My name is Miles. You are an astronomer, knowledgeable about the solar system.",
        examples=[
            language_models.InputOutputTextPair(
                input_text="How many moons does Mars have?",
                output_text="The planet Mars has two moons, Phobos and Deimos.",
            ),
        ],
    )

    responses = chat.send_message_streaming(
        message="How many planets are there in the solar system?",
        **parameters,
    )

    results = []
    for response in responses:
        print(response)
        results.append(str(response))
    results = "".join(results)
    return results


# [END aiplatform_streaming_chat]
if __name__ == "__main__":
    streaming_prediction()
