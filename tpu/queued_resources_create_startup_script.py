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

from google.cloud.tpu_v2alpha1 import Node


def create_queued_resource_startup_script(
    project_id: str,
    zone: str,
    tpu_name: str,
    tpu_type: str = "v5litepod-4",
    runtime_version: str = "v2-tpuv5-litepod",
    queued_resource_name: str = "resource-name",
) -> Node:
    # [START tpu_queued_resources_startup_script]
    from google.cloud import tpu_v2alpha1

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-a"
    # tpu_name = "tpu-name"
    # tpu_type = "v5litepod-4"
    # runtime_version = "v2-tpuv5-litepod"
    # queued_resource_name = "resource-name"

    node = tpu_v2alpha1.Node()
    node.accelerator_type = tpu_type
    # To see available runtime version use command:
    # gcloud compute tpus versions list --zone={ZONE}
    node.runtime_version = runtime_version
    # This startup script updates numpy to the latest version and logs the output to a file.
    script = {
        "startup-script": """#!/bin/bash
    echo "Hello World" > /var/log/hello.log
    sudo pip3 install --upgrade numpy >> /var/log/hello.log 2>&1
    """
    }
    node.metadata = script
    # Enabling external IPs for internet access from the TPU node for updating numpy
    node.network_config = tpu_v2alpha1.NetworkConfig(
        enable_external_ips=True,
    )

    node_spec = tpu_v2alpha1.QueuedResource.Tpu.NodeSpec()
    node_spec.parent = f"projects/{project_id}/locations/{zone}"
    node_spec.node_id = tpu_name
    node_spec.node = node

    resource = tpu_v2alpha1.QueuedResource()
    resource.tpu = tpu_v2alpha1.QueuedResource.Tpu(node_spec=[node_spec])

    request = tpu_v2alpha1.CreateQueuedResourceRequest(
        parent=f"projects/{project_id}/locations/{zone}",
        queued_resource_id=queued_resource_name,
        queued_resource=resource,
    )

    client = tpu_v2alpha1.TpuClient()
    operation = client.create_queued_resource(request=request)

    response = operation.result()
    print(response.name)
    print(response.tpu.node_spec[0].node.metadata)
    # Example response:
    # projects/[project_id]/locations/[zone]/queuedResources/resource-name
    # {'startup-script': '#!/bin/bash\n    echo "Hello World" > /var/log/hello.log\n
    # sudo pip3 install --upgrade numpy >> /var/log/hello.log 2>&1\n    '}

    # [END tpu_queued_resources_startup_script]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    create_queued_resource_startup_script(
        project_id=PROJECT_ID,
        zone=ZONE,
        tpu_name="tpu-name",
        queued_resource_name="resource-name",
    )
