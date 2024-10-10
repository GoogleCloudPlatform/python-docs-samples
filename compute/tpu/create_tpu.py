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


def create_cloud_tpu(
    project_id: str,
    zone: str,
    tpu_name: str,
    tpu_type: str = "v3-8",
    runtime_version: str = "tpu-vm-tf-2.17.0-pjrt",
) -> None:
    # [START tpu_vm_create]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # tpu_name = "tpu-name"
    # tpu_type = "v2-8"
    # runtime_version = "tpu-vm-tf-2.17.0-pjrt"

    # Create a TPU node
    node = tpu_v2.Node()
    node.accelerator_type = tpu_type
    # To see available versions use command:
    # gcloud compute tpus versions list --zone={ZONE}
    node.runtime_version = runtime_version

    # Optional. Adding metadata to the TPU node.
    # This script updates numpy to the latest version and logs the output to a file.
    metadata = {
        "startup-script": """#!/bin/bash
    echo "Hello World" > /var/log/hello.log
    sudo pip3 install --upgrade numpy >> /var/log/hello.log 2>&1
    """
    }
    node.metadata = metadata

    # Optional. Enabling external IPs for internet access from the TPU node
    node.network_config = tpu_v2.NetworkConfig(enable_external_ips=True)

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
    # accelerator_type: "v2-8"
    # state: READY
    # ...

    # [END tpu_vm_create]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-b"
    create_cloud_tpu(PROJECT_ID, ZONE, "tpu-name")
