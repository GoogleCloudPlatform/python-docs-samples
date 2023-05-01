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
# [START genappbuilder_list_documents]
from google.cloud import discoveryengine_v1beta as genappbuilder

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"
# search_engine_id = "YOUR_SEARCH_ENGINE_ID"


def list_documents_sample(
    project_id: str,
    location: str,
    search_engine_id: str
) -> None:
    # Create a client
    client = genappbuilder.DocumentServiceClient()

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        branch="default_branch",
    )

    response = client.list_documents(parent=parent)

    print(f"Documents in {search_engine_id}:")
    for result in response:
        print(result)


# [END genappbuilder_list_documents]
