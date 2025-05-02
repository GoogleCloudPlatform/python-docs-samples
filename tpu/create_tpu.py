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


def create_cloud_tpu(
    project_id: str,
    zone: str,
    tpu_name: str,
    tpu_type: str = "v5litepod-4",
    runtime_version: str = "v2-tpuv5-litepod",
) -> Node:
    """Creates a Cloud TPU node.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the TPU node will be created.
        tpu_name (str): The name of the TPU node.
        tpu_type (str, optional): The type of TPU to create.
        runtime_version (str, optional): The runtime version for the TPU.
    Returns:
        Node: The created TPU node.
    """
    # [START tpu_vm_create]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-a"
    # tpu_name = "tpu-name"
    # tpu_type = "v5litepod-4"
    # runtime_version = "v2-tpuv5-litepod"

    # Create a TPU node
    node = tpu_v2.Node()
    node.accelerator_type = tpu_type
    # To see available runtime version use command:
    # gcloud compute tpus versions list --zone={ZONE}
    node.runtime_version = runtime_version

    request = tpu_v2.CreateNodeRequest(
        parent=f"projects/{project_id}/locations/{zone}",
        node_id=tpu_name,
        node=node,
    )

    # Create a TPU client
    client = tpu_v2.TpuClient()
    operation = client.create_node(request=request)
    print("Waiting for operation to complete...")

    response = operation.result()
    print(response)
    # Example response:
    # name: "projects/[project_id]/locations/[zone]/nodes/my-tpu"
    # accelerator_type: "v5litepod-4"
    # state: READY
    # ...

    # [END tpu_vm_create]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    create_cloud_tpu(PROJECT_ID, ZONE, "tpu-name")
