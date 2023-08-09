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

# [START aiplatform_sdk_streaming_chat]
import datetime

import vertexai
from vertexai.preview.language_models import CodeGenerationModel


def streaming_prediction(
    project_id: str,
    location: str,
) -> str:
    """Streaming Chat Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    code_model = CodeGenerationModel.from_pretrained("chat-bison")
    code = code_model.start_chat()

    print("Start: ", datetime.datetime.now())
    responses = code.send_message_streaming(
        message="Write a function that checks if a year is a leap year.",
        max_output_tokens=1000)
    for response in responses:
        print(datetime.datetime.now())
        print(response)
    print("End: ", datetime.datetime.now())
    # [END aiplatform_sdk_streaming_chat]

    return responses


if __name__ == "__main__":
    streaming_prediction()