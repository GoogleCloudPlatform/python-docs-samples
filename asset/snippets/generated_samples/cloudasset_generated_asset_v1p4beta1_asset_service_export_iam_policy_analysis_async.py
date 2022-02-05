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
# Snippet for ExportIamPolicyAnalysis
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-asset


# [START cloudasset_generated_asset_v1p4beta1_AssetService_ExportIamPolicyAnalysis_async]
from google.cloud import asset_v1p4beta1


async def sample_export_iam_policy_analysis():
    # Create a client
    client = asset_v1p4beta1.AssetServiceAsyncClient()

    # Initialize request argument(s)
    analysis_query = asset_v1p4beta1.IamPolicyAnalysisQuery()
    analysis_query.parent = "parent_value"

    output_config = asset_v1p4beta1.IamPolicyAnalysisOutputConfig()
    output_config.gcs_destination.uri = "uri_value"

    request = asset_v1p4beta1.ExportIamPolicyAnalysisRequest(
        analysis_query=analysis_query,
        output_config=output_config,
    )

    # Make the request
    operation = client.export_iam_policy_analysis(request=request)

    print("Waiting for operation to complete...")

    response = await operation.result()
    print(response)

# [END cloudasset_generated_asset_v1p4beta1_AssetService_ExportIamPolicyAnalysis_async]
