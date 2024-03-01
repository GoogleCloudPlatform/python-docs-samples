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

# [START aiplatform_sdk_code_completion_test_function]
from vertexai.language_models import CodeGenerationModel


def complete_test_function(temperature: float = 0.2) -> object:
    """Example of using Codey for Code Completion to complete a test function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 64,  # Token limit determines the maximum amount of text output.
    }

    code_completion_model = CodeGenerationModel.from_pretrained("code-gecko@001")
    response = code_completion_model.predict(
        prefix="""def reverse_string(s):
            return s[::-1]
        def test_empty_input_string()""",
        **parameters,
    )

    print(f"Response from Model: {response.text}")

    return response


# [END aiplatform_sdk_code_completion_test_function]
if __name__ == "__main__":
    complete_test_function()
