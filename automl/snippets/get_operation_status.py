# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def get_operation_status(operation_full_id):
    """Get operation status."""
    # [START automl_get_operation_status]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # operation_full_id = \
    #     "projects/[projectId]/locations/us-central1/operations/[operationId]"

    client = automl.AutoMlClient()
    # Get the latest state of a long-running operation.
    response = client._transport.operations_client.get_operation(operation_full_id)

    print("Name: {}".format(response.name))
    print("Operation details:")
    print(response)
    # [END automl_get_operation_status]
