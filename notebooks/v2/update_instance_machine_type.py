# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START notebooks_v2_update_instance_machine_type]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2
from google.protobuf import field_mask_pb2


def update_instance_machine_type(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-instance",
    machine_type: str = "n1-standard-8",
) -> None:
    """Updates the machine type of a stopped Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone where the instance resides.
        instance_id: The ID of the stopped Workbench instance to update.
        machine_type: The target Compute Engine machine type.
    """
    client = notebooks_v2.NotebookServiceClient()
    name = f"projects/{project_id}/locations/{location_id}/instances/{instance_id}"
    gce_setup = notebooks_v2.GceSetup(machine_type=machine_type)
    instance = notebooks_v2.Instance(name=name, gce_setup=gce_setup)
    update_mask = field_mask_pb2.FieldMask(paths=["gce_setup.machine_type"])
    request = notebooks_v2.UpdateInstanceRequest(
        instance=instance,
        update_mask=update_mask,
    )

    try:
        operation = client.update_instance(request=request)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        response = operation.result(timeout=300)
        print(f"Resource ID: {response.name}")
        print(f"Machine Type: {response.gce_setup.machine_type}")
        print(f"State: {response.state.name}")
    except exceptions.NotFound as err:
        print(
            f"error: Instance '{instance_id}' not found in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_update_instance_machine_type]
