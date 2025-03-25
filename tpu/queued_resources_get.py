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

from google.cloud.tpu_v2alpha1 import QueuedResource


def get_queued_resource(
    project_id: str, zone: str, queued_resource_name: str
) -> QueuedResource:
    # [START tpu_queued_resources_get]
    from google.cloud import tpu_v2alpha1

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # queued_resource_name = "resource-name"

    client = tpu_v2alpha1.TpuClient()
    name = (
        f"projects/{project_id}/locations/{zone}/queuedResources/{queued_resource_name}"
    )
    resource = client.get_queued_resource(name=name)
    print("Resource name:", resource.name)
    print(resource.state)
    # Example response:
    # Resource name: projects/{project_id}/locations/{zone}/queuedResources/resource-name
    # State.ACTIVE

    # [END tpu_queued_resources_get]
    return resource


if __name__ == "__main__":
    PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
    ZONE = "us-central1-a"
    get_queued_resource(PROJECT_ID, ZONE, "resource-name")
