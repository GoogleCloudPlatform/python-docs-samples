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


def delete_cloud_tpu(project_id: str, zone: str, tpu_name: str = "tpu-name") -> None:
    """Deletes a Cloud TPU node.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the TPU node is located.
        tpu_name (str, optional): The name of the TPU node.
    Returns: None
    """
    # [START tpu_vm_delete]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-b"
    # tpu_name = "tpu-name"

    client = tpu_v2.TpuClient()
    try:
        client.delete_node(
            name=f"projects/{project_id}/locations/{zone}/nodes/{tpu_name}"
        )
        print("The TPU node was deleted.")
    except Exception as e:
        print(e)

    # [END tpu_vm_delete]


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    delete_cloud_tpu(PROJECT_ID, ZONE, "tpu-name")
