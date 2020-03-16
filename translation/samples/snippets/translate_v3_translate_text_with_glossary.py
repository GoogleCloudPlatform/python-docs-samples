# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START translate_v3_translate_text_with_glossary]

from google.cloud import translate_v3


def translate_text_with_glossary(
    text="YOUR_TEXT_TO_TRANSLATE",
    project_id="YOUR_PROJECT_ID",
    glossary_id="YOUR_GLOSSARY_ID",
):
    """Translates a given text using a glossary."""

    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(project_id, "us-central1")

    glossary = client.glossary_path(
        project_id, "us-central1", glossary_id  # The location of the glossary
    )

    glossary_config = translate_v3.types.TranslateTextGlossaryConfig(
        glossary=glossary)

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        contents=[text],
        target_language_code="ja",
        source_language_code="en",
        parent=parent,
        glossary_config=glossary_config,
    )
    print("Translated text: \n")
    for translation in response.glossary_translations:
        print(u"\t {}".format(translation.translated_text))


# [END translate_v3_translate_text_with_glossary]
