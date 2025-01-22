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

from google.cloud.tpu_v2 import Node


def create_cloud_tpu_with_topology(
    project_id: str,
    zone: str,
    tpu_name: str,
    runtime_version: str = "tpu-vm-tf-2.17.0-pjrt",
) -> Node:
    """Creates a Cloud TPU node with a specific topology.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the TPU node will be created.
        tpu_name (str): The name of the TPU node.
        runtime_version (str, optional): The runtime version for the TPU.
    Returns:
        Node: The created TPU node.
    """
    # [START tpu_vm_create_topology]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # tpu_name = "tpu-name"
    # runtime_version = "tpu-vm-tf-2.17.0-pjrt"

    node = tpu_v2.Node()
    # Here we are creating a TPU v3-8 with 2x2 topology.
    node.accelerator_config = tpu_v2.AcceleratorConfig(
        type_=tpu_v2.AcceleratorConfig.Type.V2,
        topology="2x2",
    )
    node.runtime_version = runtime_version

    request = tpu_v2.CreateNodeRequest(
        parent=f"projects/{project_id}/locations/{zone}",
        node_id=tpu_name,
        node=node,
    )

    client = tpu_v2.TpuClient()
    operation = client.create_node(request=request)
    print("Waiting for operation to complete...")

    response = operation.result()
    print(response.accelerator_config)
    # Example response:
    # type_: V3
    # topology: "2x2"

    # [END tpu_vm_create_topology]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    create_cloud_tpu_with_topology(PROJECT_ID, ZONE, "tpu-name")
