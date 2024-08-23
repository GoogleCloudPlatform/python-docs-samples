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

# [START genappbuilder_get_data_store]

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"
# data_store_id = "YOUR_DATA_STORE_ID"


def get_data_store_sample(
    project_id: str,
    location: str,
    data_store_id: str,
) -> discoveryengine.DataStore:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DataStoreServiceClient(client_options=client_options)

    request = discoveryengine.GetDataStoreRequest(
        # The full resource name of the data store
        name=client.data_store_path(project_id, location, data_store_id)
    )

    # Make the request
    data_store = client.get_data_store(request=request)

    print(data_store)

    return data_store


# [END genappbuilder_get_data_store]
