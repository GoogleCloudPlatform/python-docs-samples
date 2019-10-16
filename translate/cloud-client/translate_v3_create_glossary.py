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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "translate_v3_create_glossary")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Create Glossary
#   description: Create Glossary
#   usage: python3 translate_v3_create_glossary.py [--project "[Google Cloud Project ID]"] [--project_2 "[Your Google Cloud Project ID]"] [--glossary_id "my_glossary_id_123"]

# [START translate_v3_create_glossary]
from google.cloud import translate_v3 as translate

def sample_create_glossary(project_id, source_lang_code, target_lang_code, input_uri, glossary_id):
    """
    Create Glossary

    Args:
      glossary_id USEFUL DESCRIPTION
      This needs to inform the developer what value
      they should provide to glossary_id.
      It might even want to make a distinction between
      the full `name` and the `glossary-id`
    """

    client = translate.TranslationServiceClient()

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'glossary-id'
    location = 'us-central1'  # The location of the glossary

    name = client.glossary_path(
        project_id,
        location,
        glossary_id)
    language_codes_set = translate.types.Glossary.LanguageCodesSet(
        language_codes=[source_lang_code, target_lang_code])

    gcs_source = translate.types.GcsSource(
       input_uri=input_uri)

    input_config = translate.types.GlossaryInputConfig(
        gcs_source=gcs_source)

    glossary = translate.types.Glossary(
        name=name,
        language_codes_set=language_codes_set,
        input_config=input_config)

    parent = client.location_path(project_id, location)

    operation = client.create_glossary(parent=parent, glossary=glossary)

    result = operation.result(timeout=90)
    print('Created: {}'.format(result.name))
    print('Input Uri: {}'.format(result.input_config.gcs_source.input_uri))

# [END translate_v3_create_glossary]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    parser.add_argument(
        "--project_2", type=str, default="[Your Google Cloud Project ID]"
    )
    parser.add_argument("--glossary_id", type=str, default="my_glossary_id_123")
    parser.add_argument('--project_id')
    parser.add_argument('--source_lang_code', type=str, default="en")
    parser.add_argument('--target_lang_code', type=str, default="es")
    parser.add_argument('--input_uri')
    args = parser.parse_args()

    sample_create_glossary(args.project_id, args.source_lang_code, args.target_lang_code, 
    args.input_uri, args.glossary_id)


if __name__ == "__main__":
    main()
