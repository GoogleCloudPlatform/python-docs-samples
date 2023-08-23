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

# [START aiplatform_streaming_text]
import datetime

import vertexai
from vertexai.language_models import TextGenerationModel


def streaming_prediction(
    project_id: str,
    location: str,
) -> str:
    """Streaming Text Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    text_generation_model = TextGenerationModel.from_pretrained("text-bison")

    print("Start: ", datetime.datetime.now())
    responses = text_generation_model.predict_streaming(prompt="Count to 100", max_output_tokens=1000)
    for response in responses:
        print(datetime.datetime.now())
        print(response)
    print("End: ", datetime.datetime.now())
    # [END aiplatform_sdk_streaming_text]

    return responses.text


if __name__ == "__main__":
    streaming_prediction()
