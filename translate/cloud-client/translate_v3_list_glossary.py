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

# DO NOT EDIT! This is a generated sample ("RequestPagedAll",  "translate_v3_list_glossary")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: List Glossaries
#   description: List Glossaries
#   usage: python3 translate_v3_list_glossary.py [--project_id "[Google Cloud Project ID]"]

# [START translate_v3_list_glossary]
from google.cloud import translate

def sample_list_glossaries(project_id):
    """List Glossaries"""

    client = translate.TranslationServiceClient()

    # TODO(developer): Uncomment and set the following variables
    # project_id = '[Google Cloud Project ID]'
    location = 'us-central1'
    parent = client.location_path(project_id, location)

    # Iterate over all results
    for glossary in client.list_glossaries(parent):
        print('Name: {}'.format(glossary.name))
        print('Entry count: {}'.format(glossary.entry_count))
        print('Input uri: {}'.format(
            glossary.input_config.gcs_source.input_uri))

        # Note: You can create a glossary using one of two modes:
        # language_code_set or language_pair. When listing the information for
        # a glossary, you can only get information for the mode you used
        # when creating the glossary.
        for language_code in glossary.language_codes_set.language_codes:
            print('Language code: {}'.format(language_code))


# [END translate_v3_list_glossary]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_list_glossaries(args.project_id)


if __name__ == "__main__":
    main()
