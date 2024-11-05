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
# [START vmwareengine_list_networks]
from typing import Iterable

from google.cloud import vmwareengine_v1


def list_networks(
    project_id: str, region: str
) -> Iterable[vmwareengine_v1.VmwareEngineNetwork]:
    """
    Retrieves a list of VMware Engine networks defined in given region.

    Args:
        project_id: name of the project you want to use.
        region: name of the region for which you want to list networks.

    Returns:
        An iterable collection containing the VMWareEngineNetworks.
    """
    client = vmwareengine_v1.VmwareEngineClient()

    return client.list_vmware_engine_networks(
        parent=f"projects/{project_id}/locations/{region}"
    )


# [END vmwareengine_list_networks]
