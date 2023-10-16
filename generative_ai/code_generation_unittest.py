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

# [START aiplatform_sdk_code_generation_unittest]
import textwrap

from vertexai.language_models import CodeGenerationModel


def generate_unittest(temperature: float = 0.5) -> object:
    """Example of using Codey for Code Generation to write a unit test."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    code_generation_model = CodeGenerationModel.from_pretrained("code-bison@001")
    response = code_generation_model.predict(
        prefix=textwrap.dedent(
            """\
    Write a unit test for this function:
    def is_leap_year(year):
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    """
        ),
        **parameters,
    )

    print(f"Response from Model: {response.text}")

    return response


if __name__ == "__main__":
    generate_unittest()
# [END aiplatform_sdk_code_generation_unittest]
