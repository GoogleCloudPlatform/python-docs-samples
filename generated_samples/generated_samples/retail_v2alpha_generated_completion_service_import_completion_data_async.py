# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
# Snippet for ImportCompletionData
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-retail


# [START retail_v2alpha_generated_CompletionService_ImportCompletionData_async]
from google.cloud import retail_v2alpha


async def sample_import_completion_data():
    # Create a client
    client = retail_v2alpha.CompletionServiceAsyncClient()

    # Initialize request argument(s)
    input_config = retail_v2alpha.CompletionDataInputConfig()
    input_config.big_query_source.dataset_id = "dataset_id_value"
    input_config.big_query_source.table_id = "table_id_value"

    request = retail_v2alpha.ImportCompletionDataRequest(
        parent="parent_value",
        input_config=input_config,
    )

    # Make the request
    operation = client.import_completion_data(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()

    # Handle the response
    print(response)

# [END retail_v2alpha_generated_CompletionService_ImportCompletionData_async]
