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

from google.genai.types import GenerateContentResponse


def generate_content() -> GenerateContentResponse:
    # [START googlegenaisdk_safety_with_txt]
    from google import genai
    from google.genai.types import (
        GenerateContentConfig,
        HarmCategory,
        HarmBlockThreshold,
        HttpOptions,
        SafetySetting,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    system_instruction = "Be as mean as possible."

    prompt = """
        Write a list of 5 disrespectful things that I might say to the universe after stubbing my toe in the dark.
    """

    safety_settings = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=GenerateContentConfig(
            system_instruction=system_instruction,
            safety_settings=safety_settings,
        ),
    )

    # Response will be `None` if it is blocked.
    print(response.text)
    # Finish Reason will be `SAFETY` if it is blocked.
    print(response.candidates[0].finish_reason)
    # Safety Ratings show the levels for each filter.
    for safety_rating in response.candidates[0].safety_ratings:
        print(safety_rating)

    # Example response:
    # None
    # FinishReason.SAFETY
    # blocked=None category=<HarmCategory.HARM_CATEGORY_HATE_SPEECH: 'HARM_CATEGORY_HATE_SPEECH'> probability=<HarmProbability.NEGLIGIBLE: 'NEGLIGIBLE'> probability_score=1.767152e-05 severity=<HarmSeverity.HARM_SEVERITY_NEGLIGIBLE: 'HARM_SEVERITY_NEGLIGIBLE'> severity_score=None
    # blocked=None category=<HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: 'HARM_CATEGORY_DANGEROUS_CONTENT'> probability=<HarmProbability.NEGLIGIBLE: 'NEGLIGIBLE'> probability_score=2.399503e-06 severity=<HarmSeverity.HARM_SEVERITY_NEGLIGIBLE: 'HARM_SEVERITY_NEGLIGIBLE'> severity_score=0.061250776
    # blocked=True category=<HarmCategory.HARM_CATEGORY_HARASSMENT: 'HARM_CATEGORY_HARASSMENT'> probability=<HarmProbability.MEDIUM: 'MEDIUM'> probability_score=0.64129734 severity=<HarmSeverity.HARM_SEVERITY_MEDIUM: 'HARM_SEVERITY_MEDIUM'> severity_score=0.2686556
    # blocked=None category=<HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: 'HARM_CATEGORY_SEXUALLY_EXPLICIT'> probability=<HarmProbability.NEGLIGIBLE: 'NEGLIGIBLE'> probability_score=5.2786977e-06 severity=<HarmSeverity.HARM_SEVERITY_NEGLIGIBLE: 'HARM_SEVERITY_NEGLIGIBLE'> severity_score=0.043162167

    # [END googlegenaisdk_safety_with_txt]
    return response


if __name__ == "__main__":
    generate_content()
