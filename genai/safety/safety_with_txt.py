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
        model="gemini-2.5-flash-preview-05-20",
        contents=prompt,
        config=GenerateContentConfig(
            system_instruction=system_instruction,
            safety_settings=safety_settings,
        ),
    )

    # Response will be `None` if it is blocked.
    print(response.text)
    # Example response:
    #     None

    # Finish Reason will be `SAFETY` if it is blocked.
    print(response.candidates[0].finish_reason)
    # Example response:
    #     FinishReason.SAFETY

    # For details on all the fields in the response
    for each in response.candidates[0].safety_ratings:
        print('\nCategory: ', str(each.category))
        print('Is Blocked:', True if each.blocked else False)
        print('Probability: ', each.probability)
        print('Probability Score: ', each.probability_score)
        print('Severity:', each.severity)
        print('Severity Score:', each.severity_score)
    # Example response:
    #
    #     Category:  HarmCategory.HARM_CATEGORY_HATE_SPEECH
    #     Is Blocked: False
    #     Probability:  HarmProbability.NEGLIGIBLE
    #     Probability Score:  2.547714e-05
    #     Severity: HarmSeverity.HARM_SEVERITY_NEGLIGIBLE
    #     Severity Score: None
    #
    #     Category:  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
    #     Is Blocked: False
    #     Probability:  HarmProbability.NEGLIGIBLE
    #     Probability Score:  3.6103818e-06
    #     Severity: HarmSeverity.HARM_SEVERITY_NEGLIGIBLE
    #     Severity Score: None
    #
    #     Category:  HarmCategory.HARM_CATEGORY_HARASSMENT
    #     Is Blocked: True
    #     Probability:  HarmProbability.MEDIUM
    #     Probability Score:  0.71599233
    #     Severity: HarmSeverity.HARM_SEVERITY_MEDIUM
    #     Severity Score: 0.30782545
    #
    #     Category:  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT
    #     Is Blocked: False
    #     Probability:  HarmProbability.NEGLIGIBLE
    #     Probability Score:  1.5624657e-05
    #     Severity: HarmSeverity.HARM_SEVERITY_NEGLIGIBLE
    #     Severity Score: None
    # [END googlegenaisdk_safety_with_txt]
    return response


if __name__ == "__main__":
    generate_content()
