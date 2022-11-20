# Copyright 2021 Google LLC
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

# [START translate_v3beta1_batch_translate_document]

from google.cloud import translate_v3beta1 as translate


def batch_translate_document(
    input_uri: str,
    output_uri: str,
    project_id: str,
    timeout=180,
):

    client = translate.TranslationServiceClient()

    # The ``global`` location is not supported for batch translation
    location = "us-central1"

    # Google Cloud Storage location for the source input. This can be a single file
    # (for example, ``gs://translation-test/input.docx``) or a wildcard
    # (for example, ``gs://translation-test/*``).
    # Supported file types: https://cloud.google.com/translate/docs/supported-formats
    gcs_source = {"input_uri": input_uri}

    batch_document_input_configs = {
        "gcs_source": gcs_source,
    }
    gcs_destination = {"output_uri_prefix": output_uri}
    batch_document_output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    # Supported language codes: https://cloud.google.com/translate/docs/language
    operation = client.batch_translate_document(
        request={
            "parent": parent,
            "source_language_code": "en-US",
            "target_language_codes": ["fr-FR"],
            "input_configs": [batch_document_input_configs],
            "output_config": batch_document_output_config,
        }
    )

    print("Waiting for operation to complete...")
    response = operation.result(timeout)

    print("Total Pages: {}".format(response.total_pages))


# [END translate_v3beta1_batch_translate_document]
