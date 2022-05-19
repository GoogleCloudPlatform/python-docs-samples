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
# Snippet for AddCatalogAttribute
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-retail


# [START retail_v2alpha_generated_CatalogService_AddCatalogAttribute_sync]
from google.cloud import retail_v2alpha


def sample_add_catalog_attribute():
    # Create a client
    client = retail_v2alpha.CatalogServiceClient()

    # Initialize request argument(s)
    catalog_attribute = retail_v2alpha.CatalogAttribute()
    catalog_attribute.key = "key_value"

    request = retail_v2alpha.AddCatalogAttributeRequest(
        attributes_config="attributes_config_value",
        catalog_attribute=catalog_attribute,
    )

    # Make the request
    response = client.add_catalog_attribute(request=request)

    # Handle the response
    print(response)

# [END retail_v2alpha_generated_CatalogService_AddCatalogAttribute_sync]
