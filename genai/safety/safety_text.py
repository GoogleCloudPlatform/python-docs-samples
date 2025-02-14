# Copyright 2024 Google LLC
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


def generate_text() -> str | None:
    # [START genai_safety_text]
    from google import genai
    from google.genai.types import GenerateContentConfig
    from google.genai.types import SafetySetting

    client = genai.Client()
    model_id = "gemini-2.0-flash-exp"

    prompt = """
        Write a list of 2 disrespectful things that I might say to the universe after stubbing my toe in the dark.
    """

    safety_settings = [
        SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_ONLY_HIGH",
        ),
        SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_LOW_AND_ABOVE",
        ),
    ]

    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=GenerateContentConfig(
            safety_settings=safety_settings,
        ),
    )

    print(response.text)
    print(response.candidates[0].safety_ratings)
    # Example response:
    # 1. "Seriously, Universe?  That's the best you've got?"
    # 2. "I'm gonna need a bigger apology than that, cosmos."
    # [SafetyRating(blocked=None, category='HARM_CATEGORY_HATE_SPEECH', probability='NEGLIGIBLE', probability_score=None, severity=None, severity_score=None), ...]

    # [END genai_safety_text]
    return response.text


if __name__ == "__main__":
    generate_text()
