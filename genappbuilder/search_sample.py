# Copyright 2023 Google LLC
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

# [START genappbuilder_search]

from google.cloud import discoveryengine_v1beta as genappbuilder

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION"                    # Values: "global"
# search_engine_id = "YOUR_SEARCH_ENGINE_ID"
# serving_config_id = "default_config"          # Values: "default_config"
# search_query = "YOUR_SEARCH_QUERY"


def search_sample(
    project_id: str,
    location: str,
    search_engine_id: str,
    serving_config_id: str,
    search_query: str,
) -> None:
    # Create a client
    client = genappbuilder.SearchServiceClient()

    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = client.serving_config_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        serving_config=serving_config_id,
    )

    request = genappbuilder.SearchRequest(
        serving_config=serving_config,
        query=search_query,
    )
    response = client.search(request)
    for result in response.results:
        print(result)


# [END genappbuilder_search]
