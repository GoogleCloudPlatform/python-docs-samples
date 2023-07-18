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

# [START vmwareengine_get_vcenter_credentials]
from google.cloud import vmwareengine_v1


def get_vcenter_credentials(
    project_id: str, zone: str, private_cloud_name: str
) -> vmwareengine_v1.Credentials:
    """
    Retrieves VCenter credentials for a Private Cloud.

    Args:
        project_id: name of the project hosting the private cloud.
        zone: name of the zone hosting the private cloud.
        private_cloud_name: name of the private cloud.

    Returns:
        A Credentials object.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    credentials = client.show_vcenter_credentials(
        private_cloud=f"projects/{project_id}/locations/{zone}/privateClouds/{private_cloud_name}"
    )
    return credentials


# [END vmwareengine_get_vcenter_credentials]
