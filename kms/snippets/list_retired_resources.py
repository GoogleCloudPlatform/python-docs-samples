# Copyright 2026 Google LLC
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

# [START kms_list_retired_resources]
from google.cloud import kms


def list_retired_resources(project_id: str, location_id: str) -> list[kms.RetiredResource]:
    """
    List the retired resources in a location.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').

    Returns:
        list[RetiredResource]: The list of retired resources.
    """

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the parent location name.
    parent = client.common_location_path(project_id, location_id)

    # Call the API.
    # The API paginates, but the Python client library handles that for us.
    resources = client.list_retired_resources(request={"parent": parent})

    # Iterate over the resources and print them.
    for resource in resources:
        print(f"Retired resource: {resource.name}")

    return list(resources)


# [END kms_list_retired_resources]
