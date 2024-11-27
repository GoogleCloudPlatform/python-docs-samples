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

# [START vmwareengine_delete_legacy_network]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def delete_legacy_network(project_id: str, region: str) -> operation.Operation:
    """
    Deletes a legacy VMware Network.

    Args:
        project_id: name of the project hosting the network.
        region: region in which the legacy network is located in.

    Returns:
        An Operation object related to started network deletion operation.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    return client.delete_vmware_engine_network(
        name=f"projects/{project_id}/"
        f"locations/{region}/"
        f"vmwareEngineNetworks/{region}-default"
    )


# [END vmwareengine_delete_legacy_network]
