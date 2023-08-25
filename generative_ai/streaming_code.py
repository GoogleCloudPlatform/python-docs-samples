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

# [START aiplatform_streaming_code]
import vertexai
from vertexai.language_models import CodeGenerationModel


def streaming_prediction(
    project_id: str,
    location: str,
) -> str:
    """Streaming Code Example with a Large Language Model"""

    vertexai.init(project=project_id, location=location)

    code_generation_model = CodeGenerationModel.from_pretrained("code-bison@001")
    parameters = {
        "temperature": 0.8,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    responses = code_generation_model.predict_streaming(
        prefix="Write a function that checks if a year is a leap year.",
        # Optional:
        # max_output_tokens=1024,
        # temperature=0.0,
    )

    results = ""
    for response in responses:
        print(response)
        results += str(response)
    # [END aiplatform_streaming_code]
    return results


if __name__ == "__main__":
    streaming_prediction()
