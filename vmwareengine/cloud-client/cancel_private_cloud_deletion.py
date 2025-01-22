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

# [START vmwareengine_cancel_cloud_deletion]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def cancel_private_cloud_deletion_by_full_name(cloud_name: str) -> operation.Operation:
    """
    Cancels in progress deletion of VMware Private Cloud.

    Args:
        cloud_name: identifier of the Private Cloud you want to cancel deletion for.
            Expected format:
            projects/{project_name}/locations/{zone}/privateClouds/{cloud}

    Returns:
        An Operation object related to canceling private cloud deletion operation.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    request = vmwareengine_v1.UndeletePrivateCloudRequest()
    request.name = cloud_name
    return client.undelete_private_cloud(request)


def cancel_private_cloud_deletion(
    project_id: str, zone: str, cloud_name: str
) -> operation.Operation:
    """
    Cancels in progress deletion of VMWare Private Cloud.

    Args:
        project_id: name of the project hosting the private cloud.
        zone: zone in which the private cloud is located in.
        cloud_name: name of the private cloud to cancel deletion for.

    Returns:
        An Operation object related to canceling private cloud deletion operation.
    """
    return cancel_private_cloud_deletion_by_full_name(
        f"projects/{project_id}/locations/{zone}/privateClouds/{cloud_name}"
    )


# [END vmwareengine_cancel_cloud_deletion]
