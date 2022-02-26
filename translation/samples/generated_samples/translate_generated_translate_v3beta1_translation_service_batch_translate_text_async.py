# -*- coding: utf-8 -*-
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for BatchTranslateText
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-translate


# [START translate_generated_translate_v3beta1_TranslationService_BatchTranslateText_async]
from google.cloud import translate_v3beta1


async def sample_batch_translate_text():
    # Create a client
    client = translate_v3beta1.TranslationServiceAsyncClient()

    # Initialize request argument(s)
    input_configs = translate_v3beta1.InputConfig()
    input_configs.gcs_source.input_uri = "input_uri_value"

    output_config = translate_v3beta1.OutputConfig()
    output_config.gcs_destination.output_uri_prefix = "output_uri_prefix_value"

    request = translate_v3beta1.BatchTranslateTextRequest(
        parent="parent_value",
        source_language_code="source_language_code_value",
        target_language_codes=['target_language_codes_value_1', 'target_language_codes_value_2'],
        input_configs=input_configs,
        output_config=output_config,
    )

    # Make the request
    operation = client.batch_translate_text(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()

    # Handle the response
    print(response)

# [END translate_generated_translate_v3beta1_TranslationService_BatchTranslateText_async]
