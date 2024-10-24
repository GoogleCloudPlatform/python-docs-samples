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

from google.cloud.tpu_v2alpha1 import CreateQueuedResourceRequest, Node


def create_queued_resource(
    project_id: str,
    zone: str,
    tpu_name: str,
    tpu_type: str = "v2-8",
    runtime_version: str = "tpu-vm-tf-2.17.0-pjrt",
    queued_resource_name: str = "resource-name",
) -> Node:
    # [START tpu_queued_resources_create]
    from google.cloud import tpu_v2alpha1

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # tpu_name = "tpu-name"
    # tpu_type = "v2-8"
    # runtime_version = "tpu-vm-tf-2.17.0-pjrt"
    # queued_resource_name = "resource-name"

    node = tpu_v2alpha1.Node()
    node.accelerator_type = tpu_type
    # To see available runtime version use command:
    # gcloud compute tpus versions list --zone={ZONE}
    node.runtime_version = runtime_version

    node_spec = tpu_v2alpha1.QueuedResource.Tpu.NodeSpec()
    node_spec.parent = f"projects/{project_id}/locations/{zone}"
    node_spec.node_id = tpu_name
    node_spec.node = node

    resource = tpu_v2alpha1.QueuedResource()
    resource.tpu = tpu_v2alpha1.QueuedResource.Tpu(node_spec=[node_spec])

    request = CreateQueuedResourceRequest(
        parent=f"projects/{project_id}/locations/{zone}",
        queued_resource_id=queued_resource_name,
        queued_resource=resource,
    )

    client = tpu_v2alpha1.TpuClient()
    operation = client.create_queued_resource(request=request)

    response = operation.result()
    print(response.name)
    print(response.state.state)
    # Example response:
    # projects/[project_id]/locations/[zone]/queuedResources/resource-name
    # State.WAITING_FOR_RESOURCES

    # [END tpu_queued_resources_create]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-b"
    create_queued_resource(
        project_id=PROJECT_ID,
        zone=ZONE,
        tpu_name="tpu-name",
        queued_resource_name="resource-name",
    )
