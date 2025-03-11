# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud.tpu_v2.services.tpu.pagers import ListNodesPager


def list_cloud_tpu(project_id: str, zone: str) -> ListNodesPager:
    """List all TPU nodes in the project and zone.
    Args:
        project_id (str): The ID of Google Cloud project.
        zone (str): The zone of the TPU nodes.
    Returns:
        ListNodesPager: The list of TPU nodes.
    """
    # [START tpu_vm_list]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"

    client = tpu_v2.TpuClient()

    nodes = client.list_nodes(parent=f"projects/{project_id}/locations/{zone}")
    for node in nodes:
        print(node.name)
        print(node.state)
        print(node.accelerator_type)
    # Example response:
    # projects/[project_id]/locations/[zone]/nodes/node-name
    # State.READY
    # v2-8

    # [END tpu_vm_list]
    return nodes


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    list_cloud_tpu(PROJECT_ID, ZONE)
