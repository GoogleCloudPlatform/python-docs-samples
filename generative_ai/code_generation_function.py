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

# [START aiplatform_sdk_code_generation_function]
from vertexai.language_models import CodeGenerationModel


def generate_a_function(temperature: float = 0.5) -> object:
    """Example of using Codey for Code Generation to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    code_generation_model = CodeGenerationModel.from_pretrained("code-bison@001")
    response = code_generation_model.predict(
        prefix="Write a function that checks if a year is a leap year.", **parameters
    )

    print(f"Response from Model: {response.text}")

    return response


# [END aiplatform_sdk_code_generation_function]
if __name__ == "__main__":
    generate_a_function()
