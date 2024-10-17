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


def create_tpu_with_spot(
    project_id: str,
    zone: str,
    tpu_name: str,
    tpu_type: str = "v2-8",
    runtime_version: str = "tpu-vm-tf-2.17.0-pjrt",
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
    # [START tpu_vm_create_spot]
    from google.cloud import tpu_v2

    # TODO (developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # tpu_name = "tpu-name"
    # tpu_type = "v2-8"
    # runtime_version = "tpu-vm-tf-2.17.0-pjrt"

    # Create a TPU node
    node = tpu_v2.Node()
    node.accelerator_type = tpu_type
    # To see available runtime version use command:
    # gcloud compute tpus versions list --zone={ZONE}
    node.runtime_version = runtime_version

    # TODO: Wait for update of library to change preemptible to spot=True
    node.scheduling_config = tpu_v2.SchedulingConfig(preemptible=True)

    request = tpu_v2.CreateNodeRequest(
        parent=f"projects/{project_id}/locations/{zone}",
        node_id=tpu_name,
        node=node,
    )

    client = tpu_v2.TpuClient()
    operation = client.create_node(request=request)
    print("Waiting for operation to complete...")

    response = operation.result()

    print(response.scheduling_config)
    # Example response:
    # TODO: Update the response to include the scheduling config

    # [END tpu_vm_create_spot]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-b"
    create_tpu_with_spot(PROJECT_ID, ZONE, "tpu-with-spot")
