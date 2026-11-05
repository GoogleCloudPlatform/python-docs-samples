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

# [START notebooks_v2_create_instance_gpu]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_gpu(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-gpu-instance",
) -> None:
    """Creates a GPU-accelerated Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new GPU instance.
        instance_id: The ID to assign to the new Workbench instance.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    accelerator_config = notebooks_v2.AcceleratorConfig(
        type_=notebooks_v2.AcceleratorConfig.AcceleratorType.NVIDIA_TESLA_T4,
        core_count=1,
    )
    gpu_driver_config = notebooks_v2.GPUDriverConfig(
        enable_gpu_driver=True,
    )
    gce_setup = notebooks_v2.GceSetup(
        machine_type="n1-standard-4",
        accelerator_configs=[accelerator_config],
        gpu_driver_config=gpu_driver_config,
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
        print(f"Resource ID: {response.name}")
        print(f"Creation Date: {response.create_time}")
        print(f"Machine Type: {response.gce_setup.machine_type}")
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


# [END notebooks_v2_create_instance_gpu]
