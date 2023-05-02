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

# [START genappbuilder_poll_operation]
from time import sleep

from google.cloud import discoveryengine_v1beta as genappbuilder

from google.longrunning import operations_pb2

# TODO(developer): Uncomment these variables before running the sample.
# Example: `projects/{project}/locations/{location}/collections/{default_collection}/dataStores/{search_engine_id}/branches/{0}/operations/{operation_id}`
# operation_name = "YOUR_OPERATION_NAME"


def poll_operation_sample(operation_name: str, limit: int = 10):
    # Create a client
    client = genappbuilder.DocumentServiceClient()

    # Make GetOperation request
    request = operations_pb2.GetOperationRequest(name=operation_name)

    for _ in range(limit):
        operation = client.get_operation(request=request)
        # Print the Operation Information
        print(operation)

        # Stop polling when Operation is no longer running
        if operation.done:
            break

        # Wait 10 seconds before polling again
        sleep(10)


# [END genappbuilder_poll_operation]
