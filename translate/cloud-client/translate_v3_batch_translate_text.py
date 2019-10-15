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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "translate_v3_batch_translate_text")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Batch translate text
#   description: Batch translate text
#   usage: python3 translate_v3_batch_translate_text.py [--input_uri "gs://cloud-samples-data/text.txt"] [--output_uri "gs://YOUR_BUCKET_ID/path_to_store_results/"] [--project_id "[Google Cloud Project ID]"] [--location "us-central1"] [--source_lang en] [--target_lang ja]

# [START translate_v3_batch_translate_text]
from google.cloud import translate_v3

def sample_batch_translate_text(
    input_uri, output_uri, project_id, location, source_lang, target_lang
):
    """Batch translate text"""

    client = translate_v3.TranslationServiceClient()

    # input_uri = 'gs://cloud-samples-data/text.txt'
    # output_uri = 'gs://YOUR_BUCKET_ID/path_to_store_results/'
    # project_id = '[Google Cloud Project ID]'
    # location = 'us-central1'
    # source_lang = 'en'
    # target_lang = 'ja'
    target_language_codes = [target_lang]
    gcs_source = {"input_uri": input_uri}

    # Optional. Can be "text/plain" or "text/html".
    mime_type = "text/plain"
    input_configs_element = {"gcs_source": gcs_source, "mime_type": mime_type}
    input_configs = [input_configs_element]
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = client.location_path(project_id, location)

    operation = client.batch_translate_text(
        parent=parent,
        source_language_code=source_lang,
        target_language_codes=target_language_codes,
        input_configs=input_configs,
        output_config=output_config)

    print(u"Waiting for operation to complete...")
    response = operation.result(90)

    # Display the translation for each input text provided
    print(u"Total Characters: {}".format(response.total_characters))
    print(u"Translated Characters: {}".format(response.translated_characters))


# [END translate_v3_batch_translate_text]


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
    parser.add_argument("--source_lang", type=str, default="en")
    parser.add_argument("--target_lang", type=str, default="ja")
    args = parser.parse_args()

    sample_batch_translate_text(
        args.input_uri,
        args.output_uri,
        args.project_id,
        args.location,
        args.source_lang,
        args.target_lang,
    )


if __name__ == "__main__":
    main()
