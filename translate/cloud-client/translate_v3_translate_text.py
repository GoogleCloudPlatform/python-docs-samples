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

# DO NOT EDIT! This is a generated sample ("Request",  "translate_v3_translate_text")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Translating Text
#   description: Translating Text
#   usage: python3 translate_v3_translate_text.py [--text "Hello, world!"] [--target_language fr] [--project_id "[Google Cloud Project ID]"]

# [START translate_v3_translate_text]
from google.cloud import translate_v3


def sample_translate_text(text, target_language, project_id):
    """
    Translating Text

    Args:
      text The content to translate in string format
      target_language Required. The BCP-47 language code to use for translation.
    """

    client = translate_v3.TranslationServiceClient()

    # text = 'Text you wish to translate'
    # target_language = 'fr'
    # project_id = '[Google Cloud Project ID]'
    contents = [text]
    parent = client.location_path(project_id, "global")

    response = client.translate_text(
        parent=parent,
        contents=contents,
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='en-US',
        target_language_code=target_language)
    # Display the translation for each input text provided
    for translation in response.translations:
        print(u"Translated text: {}".format(translation.translated_text))


# [END translate_v3_translate_text]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default="Hello, world!")
    parser.add_argument("--target_language", type=str, default="fr")
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_translate_text(args.text, args.target_language, args.project_id)


if __name__ == "__main__":
    main()
