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
    # [START googlegenaisdk_thinking_budget_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, ThinkingConfig

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents="solve x^2 + 4x + 4 = 0",
        config=GenerateContentConfig(
            thinking_config=ThinkingConfig(
                thinking_budget=1024,  # Use `0` to turn off thinking
            )
        ),
    )

    print(response.text)
    # Example response:
    #     To solve the equation $x^2 + 4x + 4 = 0$, you can use several methods:
    #     **Method 1: Factoring**
    #     1.  Look for two numbers that multiply to the constant term (4) and add up to the coefficient of the $x$ term (4).
    #     2.  The numbers are 2 and 2 ($2 \times 2 = 4$ and $2 + 2 = 4$).
    #     ...
    #     ...
    #     All three methods yield the same solution. This quadratic equation has exactly one distinct solution (a repeated root).
    #     The solution is **x = -2**.

    # Token count for `Thinking`
    print(response.usage_metadata.thoughts_token_count)
    # Example response:
    #     886

    # Total token count
    print(response.usage_metadata.total_token_count)
    # Example response:
    #     1525
    # [END googlegenaisdk_thinking_budget_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
