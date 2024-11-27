# Copyright 2023 Google LLC
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

# [START vmwareengine_delete_private_cloud]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def delete_private_cloud_by_full_name(cloud_name: str) -> operation.Operation:
    """
    Deletes VMware Private Cloud.

    Args:
        cloud_name: identifier of the Private Cloud you want to delete.
            Expected format:
            projects/{project_name}/locations/{zone}/privateClouds/{cloud}

    Returns:
        An Operation object related to started private cloud deletion operation.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    request = vmwareengine_v1.DeletePrivateCloudRequest()
    request.force = True
    request.delay_hours = 3
    request.name = cloud_name
    return client.delete_private_cloud(request)


def delete_private_cloud(
    project_id: str, zone: str, cloud_name: str
) -> operation.Operation:
    """
    Deletes VMWare Private Cloud.

    Args:
        project_id: name of the project hosting the private cloud.
        zone: zone in which the private cloud is located in.
        cloud_name: name of the private cloud to be deleted.

    Returns:
        An Operation object related to started private cloud deletion operation.
    """
    return delete_private_cloud_by_full_name(
        f"projects/{project_id}/locations/{zone}/privateClouds/{cloud_name}"
    )


# [END vmwareengine_delete_private_cloud]
