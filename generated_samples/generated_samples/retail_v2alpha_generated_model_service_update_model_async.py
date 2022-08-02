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
# Snippet for UpdateModel
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-retail


# [START retail_v2alpha_generated_ModelService_UpdateModel_async]
from google.cloud import retail_v2alpha


async def sample_update_model():
    # Create a client
    client = retail_v2alpha.ModelServiceAsyncClient()

    # Initialize request argument(s)
    model = retail_v2alpha.Model()
    model.page_optimization_config.page_optimization_event_type = "page_optimization_event_type_value"
    model.page_optimization_config.panels.candidates.serving_config_id = "serving_config_id_value"
    model.page_optimization_config.panels.default_candidate.serving_config_id = "serving_config_id_value"
    model.name = "name_value"
    model.display_name = "display_name_value"
    model.type_ = "type__value"

    request = retail_v2alpha.UpdateModelRequest(
        model=model,
    )

    # Make the request
    response = await client.update_model(request=request)

    # Handle the response
    print(response)

# [END retail_v2alpha_generated_ModelService_UpdateModel_async]
