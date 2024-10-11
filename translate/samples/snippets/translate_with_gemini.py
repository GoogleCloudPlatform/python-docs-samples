# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_gemini_translate]
import os

import vertexai
from vertexai.generative_models import GenerationResponse, GenerativeModel, Part

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def translate_text(text: str, target_language_code: str = "fr") -> GenerationResponse:
    """Translates the given text to the specified target language using the Gemini model.
    Args:
        text (str): The text to be translated.
        target_language_code (str): The language code of the target language. Defaults to "fr" (French).
            Available language codes: https://cloud.google.com/translate/docs/languages#neural_machine_translation_model
    Returns:
        responses: The response from the model containing the translated text.
    """
    # Initializes the Vertex AI with the specified project and location
    vertexai.init(project=PROJECT_ID, location="europe-west2")

    model = GenerativeModel("gemini-1.0-pro")

    # Configuration for the text generation
    generation_config = {
        "candidate_count": 1,
        "max_output_tokens": 50,
        "temperature": 0.1,
        "top_k": 1,
        "top_p": 1.0,
    }

    # Creates a prompt with the text to be translated and the target language code
    promt = Part.from_text(
        f"TEXT_TO_TRANSLATE:{text}. TARGET_LANGUAGE_CODE:{target_language_code}."
    )

    responses = model.generate_content(
        contents=[promt],
        generation_config=generation_config,
    )

    print(responses.candidates[0].content.text)
    # Example response:
    # Bonjour ! Comment allez-vous aujourd'hui ?

    return responses


# [END aiplatform_gemini_translate]

if __name__ == "__main__":
    translate_text(text="Hello! How are you doing today?", target_language_code="fr")
