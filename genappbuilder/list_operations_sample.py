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

# [START genappbuilder_list_operations]
from typing import Optional

from google.cloud import discoveryengine_v1beta as genappbuilder

import google.longrunning.operations_pb2 as operations

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_PROCESSOR_LOCATION"  # Options: "global"
# search_engine_id = "YOUR_SEARCH_ENGINE_ID"

# Create filter in https://google.aip.dev/160 syntax
# operations_filter = "YOUR_FILTER"


def list_operations_sample(
    project_id: str,
    location: str,
    search_engine_id: str,
    operations_filter: Optional[str] = None,
) -> None:
    # Create a client
    client = genappbuilder.DocumentServiceClient()

    # The full resource name of the search engine branch.
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{search_engine_id}"

    # Make ListOperations request
    request = operations.ListOperationsRequest(
        name=name,
        filter=operations_filter,
    )

    # Make ListOperations request
    response = client.list_operations(request=request)

    # Print the Operation Information
    for operation in response.operations:
        print(operation)


# [END genappbuilder_list_operations]
