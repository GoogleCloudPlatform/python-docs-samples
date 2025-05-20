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
    # [START googlegenaisdk_tools_code_exec_with_txt]
    from google import genai
    from google.genai.types import (
        HttpOptions,
        Tool,
        ToolCodeExecution,
        GenerateContentConfig,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    model_id = "gemini-2.5-flash-preview-05-20"

    code_execution_tool = Tool(code_execution=ToolCodeExecution())
    response = client.models.generate_content(
        model=model_id,
        contents="Calculate 20th fibonacci number. Then find the nearest palindrome to it.",
        config=GenerateContentConfig(
            tools=[code_execution_tool],
            temperature=0,
        ),
    )
    print("# Code:")
    print(response.executable_code)
    print("# Outcome:")
    print(response.code_execution_result)

    # Example response:
    # # Code:
    # def fibonacci(n):
    #     if n <= 0:
    #         return 0
    #     elif n == 1:
    #         return 1
    #     else:
    #         a, b = 0, 1
    #         for _ in range(2, n + 1):
    #             a, b = b, a + b
    #         return b
    #
    # fib_20 = fibonacci(20)
    # print(f'{fib_20=}')
    #
    # # Outcome:
    # fib_20=6765
    # [END googlegenaisdk_tools_code_exec_with_txt]
    return response.executable_code


if __name__ == "__main__":
    generate_content()
