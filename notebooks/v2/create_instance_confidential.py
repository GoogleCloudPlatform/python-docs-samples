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

# [START notebooks_v2_create_instance_confidential]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_confidential(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-confidential-instance",
) -> None:
    """Creates a Shielded VM Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    shielded_config = notebooks_v2.ShieldedInstanceConfig(
        enable_secure_boot=True,
        enable_vtpm=True,
        enable_integrity_monitoring=True,
    )
    gce_setup = notebooks_v2.GceSetup(
        machine_type="n2d-standard-4",
        shielded_instance_config=shielded_config,
    )
    instance = notebooks_v2.Instance(gce_setup=gce_setup)
    request = notebooks_v2.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance,
    )

    try:
        operation = client.create_instance(request=request)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        # The operation completes once the instance is accepted, before the
        # VM finishes provisioning, so the state is usually PROVISIONING here.
        response = operation.result(timeout=300)
        secure_boot = response.gce_setup.shielded_instance_config.enable_secure_boot
        print(f"Resource ID: {response.name}")
        print(f"Machine Type: {response.gce_setup.machine_type}")
        print(f"Secure Boot Enabled: {secure_boot}")
        print(f"State: {response.state.name}")
        print(
            "The instance is still starting up; call get_instance until the "
            "state is ACTIVE before connecting to JupyterLab."
        )
    except exceptions.AlreadyExists as err:
        print(
            f"error: Instance '{instance_id}' already exists in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_create_instance_confidential]
