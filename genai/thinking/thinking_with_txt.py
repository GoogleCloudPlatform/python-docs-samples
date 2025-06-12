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
    # [START googlegenaisdk_thinking_with_txt]
    from google import genai

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-05-06",
        contents="solve x^2 + 4x + 4 = 0",
    )
    print(response.text)
    # Example Response:
    #     Okay, let's solve the quadratic equation x² + 4x + 4 = 0.
    #
    #     We can solve this equation by factoring, using the quadratic formula, or by recognizing it as a perfect square trinomial.
    #
    #     **Method 1: Factoring**
    #
    #     1.  We need two numbers that multiply to the constant term (4) and add up to the coefficient of the x term (4).
    #     2.  The numbers 2 and 2 satisfy these conditions: 2 * 2 = 4 and 2 + 2 = 4.
    #     3.  So, we can factor the quadratic as:
    #         (x + 2)(x + 2) = 0
    #         or
    #         (x + 2)² = 0
    #     4.  For the product to be zero, the factor must be zero:
    #         x + 2 = 0
    #     5.  Solve for x:
    #         x = -2
    #
    #     **Method 2: Quadratic Formula**
    #
    #     The quadratic formula for an equation ax² + bx + c = 0 is:
    #     x = [-b ± sqrt(b² - 4ac)] / (2a)
    #
    #     1.  In our equation x² + 4x + 4 = 0, we have a=1, b=4, and c=4.
    #     2.  Substitute these values into the formula:
    #         x = [-4 ± sqrt(4² - 4 * 1 * 4)] / (2 * 1)
    #         x = [-4 ± sqrt(16 - 16)] / 2
    #         x = [-4 ± sqrt(0)] / 2
    #         x = [-4 ± 0] / 2
    #         x = -4 / 2
    #         x = -2
    #
    #     **Method 3: Perfect Square Trinomial**
    #
    #     1.  Notice that the expression x² + 4x + 4 fits the pattern of a perfect square trinomial: a² + 2ab + b², where a=x and b=2.
    #     2.  We can rewrite the equation as:
    #         (x + 2)² = 0
    #     3.  Take the square root of both sides:
    #         x + 2 = 0
    #     4.  Solve for x:
    #         x = -2
    #
    #     All methods lead to the same solution.
    #
    #     **Answer:**
    #     The solution to the equation x² + 4x + 4 = 0 is x = -2. This is a repeated root (or a root with multiplicity 2).
    # [END googlegenaisdk_thinking_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
