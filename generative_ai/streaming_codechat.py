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

# [START aiplatform_streaming_codechat]
import vertexai
from vertexai import language_models


def streaming_prediction(
    project_id: str,
    location: str,
) -> str:
    """Streaming Code Chat Example with a Large Language Model."""

    vertexai.init(project=project_id, location=location)

    codechat_model = language_models.CodeChatModel.from_pretrained("codechat-bison")
    parameters = {
        # Temperature controls the degree of randomness in token selection.
        "temperature": 0.8,
        # Token limit determines the maximum amount of text output.
        "max_output_tokens": 1024,
    }
    codechat = codechat_model.start_chat()

    responses = codechat.send_message_streaming(
        message="Please help write a function to calculate the min of two numbers",
        **parameters,
    )

    results = []
    for response in responses:
        print(response)
        results.append(str(response))
    results = "\n".join(results)
    return results


# [END aiplatform_streaming_codechat]
if __name__ == "__main__":
    streaming_prediction()
