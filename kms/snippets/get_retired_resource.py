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

# [START kms_get_retired_resource]
from google.cloud import kms


def get_retired_resource(
    project_id: str, location_id: str, retired_resource_id: str
) -> kms.RetiredResource:
    """
    Get the details of a retired resource.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        retired_resource_id (string): ID of the retired resource to get.

    Returns:
        RetiredResource: The requested retired resource.

    """

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the retired resource name.
    # Note: Retired resources are tied to a Location, not a KeyRing.
    # The name is like projects/{project}/locations/{location}/retiredResources/{id}
    name = client.retired_resource_path(project_id, location_id, retired_resource_id)

    # Call the API.
    response = client.get_retired_resource(request={"name": name})

    print(f"Got retired resource: {response.name}")
    return response


# [END kms_get_retired_resource]
