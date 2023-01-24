# Copyright 2021 Google LLC
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
# Get a long-running operation.
# [START contactcenterinsights_get_operation]
from google.cloud import contact_center_insights_v1
from google.longrunning import operations_pb2


def get_operation(operation_name: str) -> operations_pb2.Operation:
    """Gets an operation.

    Args:
        operation_name:
            The operation name.
            Format is 'projects/{project_id}/locations/{location_id}/operations/{operation_id}'.
            For example, 'projects/my-project/locations/us-central1/operations/123456789'.

    Returns:
        An operation.
    """
    # Construct an Insights client that will authenticate via Application Default Credentials.
    # See authentication details at https://cloud.google.com/docs/authentication/production.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()

    # Call the Insights client to get the operation.
    operation = insights_client.transport.operations_client.get_operation(
        operation_name
    )
    if operation.done:
        print("Operation is done")
    else:
        print("Operation is in progress")


# [END contactcenterinsights_get_operation]
