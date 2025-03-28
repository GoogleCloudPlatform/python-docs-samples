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

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25",
        contents="solve x^2 + 4x + 4 = 0",
    )
    print(response.text)
    # Example Response:
    #     Okay, let's solve the quadratic equation x² + 4x + 4 = 0.
    #
    #     There are a few ways to solve this:
    #
    #     **Method 1: Factoring**
    #
    #     1.  **Look for two numbers** that multiply to the constant term (4) and add up to the coefficient of the x term (4).
    #         *   The numbers are 2 and 2 (since 2 * 2 = 4 and 2 + 2 = 4).
    #     2.  **Factor the quadratic** using these numbers:
    #         (x + 2)(x + 2) = 0
    #         This can also be written as:
    #         (x + 2)² = 0
    #     3.  **Set the factor equal to zero** and solve for x:
    #         x + 2 = 0
    #         x = -2
    #
    #     This type of solution, where the factor is repeated, is called a repeated root or a root with multiplicity 2.
    #
    #     **Method 2: Using the Quadratic Formula**
    #
    #     The quadratic formula solves for x in any equation of the form ax² + bx + c = 0:
    #     x = [-b ± √(b² - 4ac)] / 2a
    #
    #     1.  **Identify a, b, and c** in the equation x² + 4x + 4 = 0:
    #         *   a = 1
    #         *   b = 4
    #         *   c = 4
    #     2.  **Substitute these values into the formula:**
    #         x = [-4 ± √(4² - 4 * 1 * 4)] / (2 * 1)
    #     3.  **Simplify:**
    #         x = [-4 ± √(16 - 16)] / 2
    #         x = [-4 ± √0] / 2
    #         x = [-4 ± 0] / 2
    #     4.  **Calculate the result:**
    #         x = -4 / 2
    #         x = -2
    #
    #     Both methods give the same solution.
    #
    #     **Answer:**
    #     The solution to the equation x² + 4x + 4 = 0 is **x = -2**.
    # [END googlegenaisdk_thinking_textgen_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
