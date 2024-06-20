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

# [START genappbuilder_list_engines]
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"


def list_engines_sample(
    project_id: str,
    location: str,
) -> discoveryengine.ListEnginesResponse:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.EngineServiceClient(client_options=client_options)

    # The full resource name of the parent collection
    # e.g. projects/{project}/locations/{location}/collections/default_collection
    parent = client.collection_path(
        project=project_id,
        location=location,
        collection="default_collection",
    )

    # Make the request
    response = client.list_engines(parent=parent)

    # Handle response
    print(response)

    return response


# [END genappbuilder_list_engines]
