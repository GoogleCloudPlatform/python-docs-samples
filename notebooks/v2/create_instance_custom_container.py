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

# [START notebooks_v2_create_instance_custom_container]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_custom_container(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-container-instance",
    repository: str = "gcr.io/deeplearning-platform-release/base-cpu",
) -> None:
    """Creates a Workbench instance from a custom container.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
        repository: The container image repository URI.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    container_image = notebooks_v2.ContainerImage(
        repository=repository,
        tag="latest",
    )
    gce_setup = notebooks_v2.GceSetup(
        machine_type="e2-standard-4",
        container_image=container_image,
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
        response = operation.result()
        repo = response.gce_setup.container_image.repository
        print(f"Resource ID: {response.name}")
        print(f"Container Repository: {repo}")
        print(f"State: {response.state.name}")
    except exceptions.AlreadyExists as err:
        print(
            f"error: Instance '{instance_id}' already exists in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_create_instance_custom_container]
