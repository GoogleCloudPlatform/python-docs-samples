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

# DO NOT EDIT! This is a generated sample ("Request",  "translate_v3_list_language_names")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: List Supported Language Names and Codes
#   description: Listing supported languages with target language name
#   usage: python3 translate_v3_list_language_names.py [--language_code en] [--project_id "[Google Cloud Project ID]"]

# [START translate_v3_list_language_names]
from google.cloud import translate_v3


def sample_get_supported_languages(language_code, project_id):
    """
    Listing supported languages with target language name

    Args:
      language_code The language to use to return localized,
      human readable names of supported languages.
    """

    client = translate_v3.TranslationServiceClient()

    # language_code = 'en'
    # project_id = '[Google Cloud Project ID]'
    parent = client.location_path(project_id, "global")

    response = client.get_supported_languages(
        display_language_code=language_code, parent=parent
    )
    # List language codes of supported languages
    for language in response.languages:
        print(u"Language Code: {}".format(language.language_code))
        print(u"Display Name: {}".format(language.display_name))


# [END translate_v3_list_language_names]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--language_code", type=str, default="en")
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_get_supported_languages(args.language_code, args.project_id)


if __name__ == "__main__":
    main()
