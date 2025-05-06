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
    # [START googlegenaisdk_thinking_includethoughts_with_txt]
    from google import genai
    from google.genai.types import GenerateContentConfig, ThinkingConfig

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-05-06",
        contents="solve x^2 + 4x + 4 = 0",
        config=GenerateContentConfig(
            thinking_config=ThinkingConfig(include_thoughts=True)
        ),
    )

    print(response.text)
    # Example Response:
    #     Okay, let's solve the quadratic equation x² + 4x + 4 = 0.
    #     ...
    #     **Answer:**
    #     The solution to the equation x² + 4x + 4 = 0 is x = -2. This is a repeated root (or a root with multiplicity 2).

    for part in response.candidates[0].content.parts:
        if part and part.thought:  # show thoughts
            print(part.text)
    # Example Response:
    #     **My Thought Process for Solving the Quadratic Equation**
    #
    #     Alright, let's break down this quadratic, x² + 4x + 4 = 0. First things first:
    #     it's a quadratic; the x² term gives it away, and we know the general form is
    #     ax² + bx + c = 0.
    #
    #     So, let's identify the coefficients: a = 1, b = 4, and c = 4. Now, what's the
    #     most efficient path to the solution? My gut tells me to try factoring; it's
    #     often the fastest route if it works. If that fails, I'll default to the quadratic
    #     formula, which is foolproof. Completing the square? It's good for deriving the
    #     formula or when factoring is difficult, but not usually my first choice for
    #     direct solving, but it can't hurt to keep it as an option.
    #
    #     Factoring, then. I need to find two numbers that multiply to 'c' (4) and add
    #     up to 'b' (4). Let's see... 1 and 4 don't work (add up to 5). 2 and 2? Bingo!
    #     They multiply to 4 and add up to 4. This means I can rewrite the equation as
    #     (x + 2)(x + 2) = 0, or more concisely, (x + 2)² = 0. Solving for x is now
    #     trivial: x + 2 = 0, thus x = -2.
    #
    #     Okay, just to be absolutely certain, I'll run the quadratic formula just to
    #     double-check. x = [-b ± √(b² - 4ac)] / 2a. Plugging in the values, x = [-4 ±
    #     √(4² - 4 * 1 * 4)] / (2 * 1). That simplifies to x = [-4 ± √0] / 2. So, x =
    #     -2 again – a repeated root. Nice.
    #
    #     Now, let's check via completing the square. Starting from the same equation,
    #     (x² + 4x) = -4. Take half of the b-value (4/2 = 2), square it (2² = 4), and
    #     add it to both sides, so x² + 4x + 4 = -4 + 4. Which simplifies into (x + 2)²
    #     = 0. The square root on both sides gives us x + 2 = 0, therefore x = -2, as
    #      expected.
    #
    #     Always, *always* confirm! Let's substitute x = -2 back into the original
    #     equation: (-2)² + 4(-2) + 4 = 0. That's 4 - 8 + 4 = 0. It checks out.
    #
    #     Conclusion: the solution is x = -2. Confirmed.
    # [END googlegenaisdk_thinking_includethoughts_with_txt]
    return response.text


if __name__ == "__main__":
    generate_content()
