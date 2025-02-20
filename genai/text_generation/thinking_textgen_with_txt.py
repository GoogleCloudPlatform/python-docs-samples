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
    # [START googlegenaisdk_thinking_textgen_with_txt]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.0-flash-thinking-exp-01-21",
        contents="solve x^2 + 4x + 4 = 0",
    )
    print(response.text)
    # Example response:
    #     To solve the equation x^2 + 4x + 4 = 0, we can use several methods.
    #
    #     **Method 1: Factoring**
    #
    #     We look for two numbers that multiply to 4 (the constant term) and add to 4 (the coefficient of the x term).
    #     These two numbers are 2 and 2 because 2 * 2 = 4 and 2 + 2 = 4.
    #     Therefore, we can factor the quadratic expression as:
    #     (x + 2)(x + 2) = 0
    #     This can also be written as:
    #     (x + 2)^2 = 0
    #
    #     To solve for x, we set the factor (x + 2) equal to zero:
    #     x + 2 = 0
    #     Subtract 2 from both sides:
    #     x = -2
    #
    #     **Method 2: Quadratic Formula**
    #
    #     The quadratic formula for an equation of the form ax^2 + bx + c = 0 is given by:
    #     x = [-b ± sqrt(b^2 - 4ac)] / (2a)
    #
    #     ...
    #
    #
    #     All three methods yield the same solution, x = -2.
    #     This is a repeated root, which is expected since the discriminant (b^2 - 4ac) is 0.
    #
    #     To check our solution, we substitute x = -2 back into the original equation:
    #     (-2)^2 + 4(-2) + 4 = 4 - 8 + 4 = 0
    #     The equation holds true, so our solution is correct.

    #     Final Answer: The final answer is $\boxed{-2}$

    # [END googlegenaisdk_thinking_textgen_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
