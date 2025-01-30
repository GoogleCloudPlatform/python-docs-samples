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
import os

from vertexai.generative_models import GenerationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def generate_translation() -> GenerationResponse:
    # [START generativeaionvertexai_text_generation_gemini_translate]
    import vertexai

    from vertexai.generative_models import GenerativeModel, HarmBlockThreshold, HarmCategory

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = GenerativeModel("gemini-1.5-flash-002")

    prompt = """
    Translate the text from source to target language and return the translated text.

    TEXT: Google's Generative AI API lets you use a large language model (LLM) to dynamically translate text.
    SOURCE_LANGUAGE_CODE: EN
    TARGET_LANGUAGE_CODE: FR
    """

    # Check the API reference for details:
    # https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#generationconfig
    generation_config = {
        "candidate_count": 1,
        "max_output_tokens": 8192,
        "temperature": 0.2,
        "top_k": 40.0,
        "top_p": 0.95,
    }
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    # Send request to Gemini
    response = model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    print(f"Translation:\n{response.text}", )
    print(f"Usage metadata:\n{response.usage_metadata}")
    # Example response:
    #     Translation:
    #     L'API d'IA générative de Google vous permet d'utiliser un grand modèle linguistique (LLM) pour traduire dynamiquement du texte.
    #
    #     Usage metadata:
    #     prompt_token_count: 63
    #     candidates_token_count: 32
    #     total_token_count: 95

    # [END generativeaionvertexai_text_generation_gemini_translate]
    return response


if __name__ == "__main__":
    generate_translation()
