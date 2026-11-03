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

# [START notebooks_v2_create_instance_private_vpc]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_private_vpc(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-private-instance",
    network_id: str = "example-network",
    subnet_id: str = "example-subnet",
) -> None:
    """Creates a Workbench instance with private IP in a custom VPC subnet.

    Disabling the external public IP address isolates the Workbench instance
    from the public internet while allowing private connectivity through a
    custom VPC network and Cloud NAT or Private Google Access.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
        network_id: The ID of the VPC network in the project.
        subnet_id: The ID of the subnetwork in the instance region.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    parts = location_id.split("-")
    region_id = "-".join(parts[:-1]) if len(parts) > 2 else location_id
    network = f"projects/{project_id}/global/networks/{network_id}"
    subnet = f"projects/{project_id}/regions/{region_id}/subnetworks/{subnet_id}"
    network_interface = notebooks_v2.NetworkInterface(
        network=network,
        subnet=subnet,
        nic_type=notebooks_v2.NetworkInterface.NicType.GVNIC,
    )
    gce_setup = notebooks_v2.GceSetup(
        machine_type="e2-standard-4",
        disable_public_ip=True,
        network_interfaces=[network_interface],
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
        response = operation.result()
        print(f"Resource ID: {response.name}")
        print(f"Creation Date: {response.create_time}")
        print(f"Disable Public IP: {response.gce_setup.disable_public_ip}")
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


# [END notebooks_v2_create_instance_private_vpc]
