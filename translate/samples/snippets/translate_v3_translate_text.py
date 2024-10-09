# Copyright 2020 Google LLC
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

# [START translate_v3_translate_text]
# Imports the Google Cloud Translation library
import os

from google.cloud import translate_v3

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


# Initialize Translation client
def translate_text(
    text: str = "YOUR_TEXT_TO_TRANSLATE",
    language_code: str = "fr",
) -> translate_v3.TranslationServiceClient:
    """Translating Text from English.
    Args:
        text: The content to translate.
        language_code: The language code for the translation.
            E.g. "fr" for French, "es" for Spanish, etc.
            Available languages: https://cloud.google.com/translate/docs/languages#neural_machine_translation_model
    """

    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"
    # Translate text from English to chosen language
    # Supported mime types: # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        contents=[text],
        target_language_code=language_code,
        parent=parent,
        mime_type="text/plain",
        source_language_code="en-US",
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")
    # Example response:
    # Translated text: Bonjour comment vas-tu aujourd'hui?

    return response


# [END translate_v3_translate_text]

if __name__ == "__main__":
    translate_text(text="Hello! How are you doing today?", language_code="fr")
