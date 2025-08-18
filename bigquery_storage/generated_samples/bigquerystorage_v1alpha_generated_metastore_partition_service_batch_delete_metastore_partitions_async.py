# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
# Snippet for BatchDeleteMetastorePartitions
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-bigquery-storage


# [START bigquerystorage_v1alpha_generated_MetastorePartitionService_BatchDeleteMetastorePartitions_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import bigquery_storage_v1alpha


async def sample_batch_delete_metastore_partitions():
    # Create a client
    client = bigquery_storage_v1alpha.MetastorePartitionServiceAsyncClient()

    # Initialize request argument(s)
    partition_values = bigquery_storage_v1alpha.MetastorePartitionValues()
    partition_values.values = ["values_value1", "values_value2"]

    request = bigquery_storage_v1alpha.BatchDeleteMetastorePartitionsRequest(
        parent="parent_value",
        partition_values=partition_values,
    )

    # Make the request
    await client.batch_delete_metastore_partitions(request=request)


# [END bigquerystorage_v1alpha_generated_MetastorePartitionService_BatchDeleteMetastorePartitions_async]
