# Copyright 2024 Google LLC
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

# [START genappbuilder_update_serving_config]

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1alpha as discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"
# engine_id = "YOUR_DATA_STORE_ID"


def update_serving_config_sample(
    project_id: str,
    location: str,
    engine_id: str,
) -> discoveryengine.ServingConfig:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )
    # Create a client
    client = discoveryengine.ServingConfigServiceClient(client_options=client_options)

    # The full resource name of the serving config
    serving_config_name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_search"

    update_mask = "customFineTuningSpec.enableSearchAdaptor"

    serving_config = client.update_serving_config(
        request=discoveryengine.UpdateServingConfigRequest(
            serving_config=discoveryengine.ServingConfig(
                name=serving_config_name,
                custom_fine_tuning_spec=discoveryengine.CustomFineTuningSpec(
                    enable_search_adaptor=True  # Switch to `False` to disable tuned model
                ),
            ),
            update_mask=update_mask,
        )
    )

    # Handle the response
    print(serving_config)

    return serving_config


# [END genappbuilder_update_serving_config]
