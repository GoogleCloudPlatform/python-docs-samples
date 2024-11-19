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

# [START genappbuilder_search_lite]

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION"          # Values: "global", "us", "eu"
# engine_id = "YOUR_APP_ID"
# api_key = "YOUR_API_KEY"
# search_query = "YOUR_SEARCH_QUERY"


def search_lite_sample(
    project_id: str,
    location: str,
    engine_id: str,
    api_key: str,
    search_query: str,
) -> discoveryengine.services.search_service.pagers.SearchLitePager:

    client_options = ClientOptions(
        # For information on API Keys, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/migrate-from-cse#api-key-deploy
        api_key=api_key,
        #  For more information, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
        api_endpoint=(
            f"{location}-discoveryengine.googleapis.com"
            if location != "global"
            else None
        ),
    )

    # Create a client
    client = discoveryengine.SearchServiceClient(client_options=client_options)

    # The full resource name of the search app serving config
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    # Refer to the `SearchRequest` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
    )

    page_result = client.search_lite(request)

    # Handle the response
    for response in page_result:
        print(response)

    return page_result


# [END genappbuilder_search_lite]
