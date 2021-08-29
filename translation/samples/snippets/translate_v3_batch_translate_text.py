# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START translate_v3_batch_translate_text]
from google.cloud import translate


def batch_translate_text(
    input_uri="gs://YOUR_BUCKET_ID/path/to/your/file.txt",
    output_uri="gs://YOUR_BUCKET_ID/path/to/save/results/",
    project_id="YOUR_PROJECT_ID",
    timeout=180,
):
    """Translates a batch of texts on GCS and stores the result in a GCS location."""

    client = translate.TranslationServiceClient()

    location = "us-central1"
    # Supported file types: https://cloud.google.com/translate/docs/supported-formats
    gcs_source = {"input_uri": input_uri}

    input_configs_element = {
        "gcs_source": gcs_source,
        "mime_type": "text/plain",  # Can be "text/plain" or "text/html".
    }
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    operation = client.batch_translate_text(
        request={
            "parent": parent,
            "source_language_code": "en",
            "target_language_codes": ["ja"],  # Up to 10 language codes here.
            "input_configs": [input_configs_element],
            "output_config": output_config,
        }
    )

    print("Waiting for operation to complete...")
    response = operation.result(timeout)

    print("Total Characters: {}".format(response.total_characters))
    print("Translated Characters: {}".format(response.translated_characters))


# [END translate_v3_batch_translate_text]
