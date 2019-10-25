# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

# DO NOT EDIT! This is a generated sample ("Request",  "translate_v3_translate_text_with_glossary")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Translating Text with Glossary
#   description: Translates a given text using a glossary.
#   usage: python3 translate_v3_translate_text_with_glossary.py [--text "Hello, world!"] [--source_language en] [--target_language fr] [--project_id "[Google Cloud Project ID]"] [--glossary_id "[YOUR_GLOSSARY_ID]"]

# [START translate_v3_translate_text_with_glossary]
from google.cloud import translate

def sample_translate_text_with_glossary(
    text, source_language, target_language, project_id, glossary_id
):
    """
    Translates a given text using a glossary.

    Args:
      text The content to translate in string format
      source_language Optional. The BCP-47 language code of the input text.
      target_language Required. The BCP-47 language code to use for translation.
      glossary_id Specifies the glossary used for this translation.
    """

    client = translate.TranslationServiceClient()

    # TODO(developer): Uncomment and set the following variables
    # text = 'Hello, world!'
    # source_language = 'en'
    # target_language = 'fr'
    # project = '[Google Cloud Project ID]'
    # glossary_id = '[YOUR_GLOSSARY_ID]'
    contents = [text]
    parent = client.location_path(project_id, "us-central1")

    glossary = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_id)
        
    glossary_config = translate.types.TranslateTextGlossaryConfig(
        glossary=glossary)

    response = client.translate_text(
        contents,
        target_language_code=target_language,
        source_language_code=source_language,
        parent=parent,
        glossary_config=glossary_config,
        mime_type='text/plain'  # mime types: text/plain, text/html
    )

    for translation in response.glossary_translations:
        print(u"Translated text: {}".format(translation.translated_text))

# [END translate_v3_translate_text_with_glossary]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default="Hello, world!")
    parser.add_argument("--source_language", type=str, default="en")
    parser.add_argument("--target_language", type=str, default="fr")
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    parser.add_argument(
        "--glossary_id",
        type=str,
        default="[YOUR_GLOSSARY_ID]",
    )
    args = parser.parse_args()

    sample_translate_text_with_glossary(
        args.text,
        args.source_language,
        args.target_language,
        args.project_id,
        args.glossary_id
    )


if __name__ == "__main__":
    main()
