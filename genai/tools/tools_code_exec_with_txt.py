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
    # [START genai_function_calling_code_execution]
    from google import genai
    from google.genai.types import Tool, ToolCodeExecution, GenerateContentConfig

    client = genai.Client()
    model_id = "gemini-2.0-flash-exp"

    code_execution_tool = Tool(code_execution=ToolCodeExecution())
    response = client.models.generate_content(
        model=model_id,
        contents="Calculate 20th fibonacci number. Then find the nearest palindrome to it.",
        config=GenerateContentConfig(
            tools=[code_execution_tool],
            temperature=0,
        ),
    )
    for part in response.candidates[0].content.parts:
        if part.executable_code:
            print(part.executable_code)
        if part.code_execution_result:
            print(part.code_execution_result)
    # Example response:
    # code='...' language='PYTHON'
    # outcome='OUTCOME_OK' output='The 20th Fibonacci number is: 6765\n'
    # code='...' language='PYTHON'
    # outcome='OUTCOME_OK' output='Lower Palindrome: 6666\nHigher Palindrome: 6776\nNearest Palindrome to 6765: 6776\n'

    # [END genai_function_calling_code_execution]
    return str(response.candidates[0].content.parts)


if __name__ == "__main__":
    generate_content()
