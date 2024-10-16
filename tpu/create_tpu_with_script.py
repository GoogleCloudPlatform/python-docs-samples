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


def create_cloud_tpu_with_script(
    project_id: str,
    zone: str,
    tpu_name: str,
    tpu_type: str = "v2-8",
    runtime_version: str = "tpu-vm-tf-2.17.0-pjrt",
) -> Node:
    # [START tpu_vm_create_startup_script]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # tpu_name = "tpu-name"
    # tpu_type = "v2-8"
    # runtime_version = "tpu-vm-tf-2.17.0-pjrt"

    node = tpu_v2.Node()
    node.accelerator_type = tpu_type
    node.runtime_version = runtime_version

    # This startup script updates numpy to the latest version and logs the output to a file.
    metadata = {
        "startup-script": """#!/bin/bash
    echo "Hello World" > /var/log/hello.log
    sudo pip3 install --upgrade numpy >> /var/log/hello.log 2>&1
    """
    }

    # Adding metadata with startup script to the TPU node.
    node.metadata = metadata
    # Enabling external IPs for internet access from the TPU node.
    node.network_config = tpu_v2.NetworkConfig(enable_external_ips=True)

    request = tpu_v2.CreateNodeRequest(
        parent=f"projects/{project_id}/locations/{zone}",
        node_id=tpu_name,
        node=node,
    )

    client = tpu_v2.TpuClient()
    operation = client.create_node(request=request)
    print("Waiting for operation to complete...")

    response = operation.result()
    print(response.metadata)
    # Example response:
    # {'startup-script': '#!/bin/bash\n    echo "Hello World" > /var/log/hello.log\n
    # ...

    # [END tpu_vm_create_startup_script]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-b"
    create_cloud_tpu_with_script(PROJECT_ID, ZONE, "tpu-name")
