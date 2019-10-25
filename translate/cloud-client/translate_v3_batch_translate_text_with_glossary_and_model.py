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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "translate_v3_batch_translate_text_with_glossary_and_model")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Batch Translate with Glossary and Model
#   description: Batch translate text with Glossary using AutoML Translation model
#   usage: python3 translate_v3_batch_translate_text_with_glossary_and_model.py [--input_uri "gs://cloud-samples-data/text.txt"] [--output_uri "gs://YOUR_BUCKET_ID/path_to_store_results/"] [--project "[Google Cloud Project ID]"] [--location "us-central1"] [--target_language en] [--source_language de] [--model_id "{your-model-id}"] [--glossary_id "{your-glossary-id}"]

# [START translate_v3_batch_translate_text_with_glossary_and_model]
from google.cloud import translate

def sample_batch_translate_text_with_glossary_and_model(
    input_uri,
    output_uri,
    project_id,
    location,
    target_language,
    source_language,
    model_id,
    glossary_id
):
    """
    Batch translate text with Glossary and Translation model
    """

    client = translate.TranslationServiceClient()

    # TODO(developer): Uncomment and set the following variables
    # input_uri = 'gs://cloud-samples-data/text.txt'
    # output_uri = 'gs://YOUR_BUCKET_ID/path_to_store_results/'
    # project = '[Google Cloud Project ID]'
    # location = 'us-central1'
    # target_language = 'en'
    # source_language = 'de'
    # model_id = '{your-model-id}'
    # glossary_id = '[YOUR_GLOSSARY_ID]'
    target_language_codes = [target_language]
    gcs_source = {"input_uri": input_uri}

    # Optional. Can be "text/plain" or "text/html".
    mime_type = "text/plain"
    input_configs_element = {"gcs_source": gcs_source, "mime_type": mime_type}
    input_configs = [input_configs_element]
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = client.location_path(project_id, location)
    model_path = 'projects/{}/locations/{}/models/{}'.format(project_id, 'us-central1', model_id)
    models = {target_language: model_path}

    glossary_path = client.glossary_path(
        project_id,
        'us-central1',  # The location of the glossary
        glossary_id)
        
    glossary_config = translate.types.TranslateTextGlossaryConfig(
        glossary=glossary_path)
    glossaries = {"ja": glossary_config} #target lang as key

    operation = client.batch_translate_text(
        parent=parent,
        source_language_code=source_language,
        target_language_codes=target_language_codes,
        input_configs=input_configs,
        output_config=output_config,
        models=models,
        glossaries=glossaries
    )

    print(u"Waiting for operation to complete...")
    response = operation.result()

    # Display the translation for each input text provided
    print(u"Total Characters: {}".format(response.total_characters))
    print(u"Translated Characters: {}".format(response.translated_characters))


# [END translate_v3_batch_translate_text_with_glossary_and_model]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_uri", type=str, default="gs://cloud-samples-data/text.txt"
    )
    parser.add_argument(
        "--output_uri", type=str, default="gs://YOUR_BUCKET_ID/path_to_store_results/"
    )
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--location", type=str, default="us-central1")
    parser.add_argument("--target_language", type=str, default="en")
    parser.add_argument("--source_language", type=str, default="de")
    parser.add_argument(
        "--model_id",
        type=str,
        default="{your-model-id}"
    )
    parser.add_argument(
        "--glossary_id",
        type=str,
        default="[YOUR_GLOSSARY_ID]",
    )
    args = parser.parse_args()

    sample_batch_translate_text_with_glossary_and_model(
        args.input_uri,
        args.output_uri,
        args.project_id,
        args.location,
        args.target_language,
        args.source_language,
        args.model_id,
        args.glossary_id
    )


if __name__ == "__main__":
    main()
