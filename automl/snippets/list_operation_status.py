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


def list_operation_status(project_id):
    """List operation status."""
    # [START automl_list_operation_status]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = "YOUR_PROJECT_ID"

    client = automl.AutoMlClient()
    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"
    # List all the operations names available in the region.
    response = client._transport.operations_client.list_operations(
        name=project_location, filter_="", timeout=5
    )

    print("List of operations:")
    for operation in response:
        print("Name: {}".format(operation.name))
        print("Operation details:")
        print(operation)
    # [END automl_list_operation_status]
