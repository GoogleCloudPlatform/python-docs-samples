# Copyright 2025 Google LLC
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


def generate_content() -> str:
    # [START googlegenaisdk_interactions_tools_code_exec_with_txt]
    from google import genai

    client = genai.Client()
    model_id = "gemini-3.8-flash"

    interaction = client.interactions.create(
        model=model_id,
        input="Calculate 20th fibonacci number. Then find the nearest palindrome to it.",
        tools=[{"type": "code_execution"}],
    )

    executable_code = None
    execution_result = None
    for step in interaction.steps:
        if step.type == "code_execution_call":
            executable_code = step.arguments.code
            print("# Code:")
            print(executable_code)
        elif step.type == "code_execution_result":
            execution_result = step.result
            print("# Outcome:")
            print(execution_result)

    print(interaction.output_text)
    # [END googlegenaisdk_interactions_tools_code_exec_with_txt]
    return executable_code


if __name__ == "__main__":
    generate_content()
