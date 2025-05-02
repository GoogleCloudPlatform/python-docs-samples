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


def stop_cloud_tpu(project_id: str, zone: str, tpu_name: str = "tpu-name") -> Node:
    """Stop a TPU node.
    Args:
        project_id (str): The ID of Google Cloud project.
        zone (str): The zone of the TPU node.
        tpu_name (str): The name of the TPU node to stop.
    Returns:
        Node: The stopped TPU node.
    """

    # [START tpu_vm_stop]
    from google.cloud import tpu_v2

    # TODO(developer): Update and un-comment below lines
    # project_id = "your-project-id"
    # zone = "us-central1-a"
    # tpu_name = "tpu-name"

    client = tpu_v2.TpuClient()

    request = tpu_v2.StopNodeRequest(
        name=f"projects/{project_id}/locations/{zone}/nodes/{tpu_name}",
    )
    try:
        operation = client.stop_node(request=request)
        print("Waiting for stop operation to complete...")
        response = operation.result()
        print(f"This TPU {tpu_name} has been stopped")
        print(response.state)
        # Example response:
        # State.STOPPED

    except Exception as e:
        print(e)
        raise e

    # [END tpu_vm_stop]
    return response


if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    ZONE = "us-central1-a"
    stop_cloud_tpu(PROJECT_ID, ZONE, "tpu-name")
