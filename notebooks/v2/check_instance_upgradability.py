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

# [START notebooks_v2_check_instance_upgradability]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def check_instance_upgradability(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
) -> None:
    """Checks whether a Workbench instance can be upgraded.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the Workbench instance to check.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    request = notebooks_v2.CheckInstanceUpgradabilityRequest(
        notebook_instance=name,
    )

    try:
        response = client.check_instance_upgradability(request=request)
        print(f"Resource ID: {name}")
        print(f"Upgrade Image: {response.upgrade_image}")
        print(f"Upgrade Info: {response.upgrade_info}")
        print(f"Upgrade Version: {response.upgrade_version}")
        print(f"Upgradeable: {response.upgradeable}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_check_instance_upgradability]
