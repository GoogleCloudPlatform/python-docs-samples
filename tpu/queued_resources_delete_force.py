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


def delete_force_queued_resource(
    project_id: str, zone: str, queued_resource_name: str
) -> None:
    # [START tpu_queued_resources_delete_force]
    from google.cloud import tpu_v2alpha1

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # queued_resource_name = "resource-name"

    client = tpu_v2alpha1.TpuClient()
    request = tpu_v2alpha1.DeleteQueuedResourceRequest(
        name=f"projects/{project_id}/locations/{zone}/queuedResources/{queued_resource_name}",
        force=True,  # Set force=True to delete the resource with tpu nodes.
    )

    try:
        op = client.delete_queued_resource(request=request)
        op.result()
        print(f"Queued resource '{queued_resource_name}' successfully deleted.")
    except TypeError as e:
        print(f"Error deleting resource: {e}")
        print(f"Queued resource '{queued_resource_name}' successfully deleted.")

    # [END tpu_queued_resources_delete_force]


if __name__ == "__main__":
    PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
    ZONE = "us-central1-a"
    delete_force_queued_resource(PROJECT_ID, ZONE, "resource-name")
