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

from google.cloud.tpu_v2alpha1.services.tpu.pagers import ListQueuedResourcesPager


def list_queued_resources(project_id: str, zone: str) -> ListQueuedResourcesPager:
    # [START tpu_queued_resources_list]
    from google.cloud import tpu_v2alpha1

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"

    client = tpu_v2alpha1.TpuClient()
    parent = f"projects/{project_id}/locations/{zone}"
    resources = client.list_queued_resources(parent=parent)
    for resource in resources:
        print("Resource name:", resource.name)
        print("TPU id:", resource.tpu.node_spec[0].node_id)
    # Example response:
    # Resource name: projects/{project_id}/locations/{zone}/queuedResources/resource-name
    # TPU id: tpu-name

    # [END tpu_queued_resources_list]
    return resources


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    list_queued_resources(PROJECT_ID, ZONE)
