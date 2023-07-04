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

# [START vmwareengine_create_legacy_network]
from google.cloud import vmwareengine_v1

TIMEOUT = 1200  # 20 minutes


def create_legacy_network(
    project_id: str, region: str
) -> vmwareengine_v1.VmwareEngineNetwork:
    """
    Creates a new legacy network.

    Args:
        project_id: name of the project you want to use.
        region: name of the region you want to use. I.e. "us-central1"

    Returns:
        The newly created VmwareEngineNetwork object.
    """
    network = vmwareengine_v1.VmwareEngineNetwork()
    network.description = (
        "Legacy network created using vmwareengine_v1.VmwareEngineNetwork"
    )
    network.type_ = vmwareengine_v1.VmwareEngineNetwork.Type.LEGACY

    request = vmwareengine_v1.CreateVmwareEngineNetworkRequest()
    request.parent = f"projects/{project_id}/locations/{region}"
    request.vmware_engine_network_id = f"{region}-default"
    request.vmware_engine_network = network

    client = vmwareengine_v1.VmwareEngineClient()
    result = client.create_vmware_engine_network(request, timeout=TIMEOUT).result()

    return result


# [END vmwareengine_create_legacy_network]
