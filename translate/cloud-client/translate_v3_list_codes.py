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

# DO NOT EDIT! This is a generated sample ("Request",  "translate_v3_list_codes")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: List Supported Language Codes
#   description: Getting a list of supported language codes
#   usage: python3 translate_v3_list_codes.py [--project_id "[Google Cloud Project ID]"]

# [START translate_v3_list_codes]
from google.cloud import translate_v3

def sample_get_supported_languages(project_id):
    """Getting a list of supported language codes"""

    client = translate_v3.TranslationServiceClient()

    # project = '[Google Cloud Project ID]'
    parent = client.location_path(project_id, "global")

    response = client.get_supported_languages(parent=parent)

    # List language codes of supported languages
    print('Supported Languages:')
    for language in response.languages:
        print(u"Language Code: {}".format(language.language_code))


# [END translate_v3_list_codes]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_get_supported_languages(args.project_id)


if __name__ == "__main__":
    main()
