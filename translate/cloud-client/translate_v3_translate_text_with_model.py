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

# DO NOT EDIT! This is a generated sample ("Request",  "translate_v3_translate_text_with_model")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Translating Text with Model
#   description: Translating Text with Model
#   usage: python3 translate_v3_translate_text_with_model.py [--model_id "[MODEL ID]"] [--text "Hello, world!"] [--target_language fr] [--source_language en] [--project_id "[Google Cloud Project ID]"] [--location global]

# [START translate_v3_translate_text_with_model]
from google.cloud import translate_v3


def sample_translate_text_with_model(
    model_id, text, target_language, source_language, project_id, location
):
    """
    Translating Text with Model

    Args:
      model_id The `model` type requested for this translation.
      text The content to translate in string format
      target_language Required. The BCP-47 language code to use for translation.
      source_language Optional. The BCP-47 language code of the input text.
    """

    client = translate_v3.TranslationServiceClient()

    # TODO(developer): Uncomment and set the following variables
    # model_id = '[MODEL ID]'
    # text = 'Hello, world!'
    # target_language = 'fr'
    # source_language = 'en'
    # project_id = '[Google Cloud Project ID]'
    # location = 'global'
    contents = [text]
    parent = client.location_path(project_id, location)
    model_path = 'projects/{}/locations/{}/models/{}'.format(project_id, 'us-central1', model_id)
    response = client.translate_text(
        contents,
        target_language,
        model=model_path,
        source_language_code=source_language,
        parent=parent,
        mime_type='text/plain'  # mime types: text/plain, text/html
    )
    # Display the translation for each input text provided
    for translation in response.translations:
        print(u"Translated text: {}".format(translation.translated_text))


# [END translate_v3_translate_text_with_model]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_id",
        type=str,
        default="[MODEL ID]",
    )
    parser.add_argument("--text", type=str, default="Hello, world!")
    parser.add_argument("--target_language", type=str, default="fr")
    parser.add_argument("--source_language", type=str, default="en")
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--location", type=str, default="global")
    args = parser.parse_args()

    sample_translate_text(
        args.model_id,
        args.text,
        args.target_language,
        args.source_language,
        args.project_id,
        args.location,
    )


if __name__ == "__main__":
    main()
