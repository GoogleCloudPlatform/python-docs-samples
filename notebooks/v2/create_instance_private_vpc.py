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

import argparse
import sys

# [START notebooks_v2_create_instance_private_vpc]
from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_private_vpc(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-private-instance",
    network_id: str = "example-network",
    subnet_id: str = "example-subnet",
) -> None:
    """Creates a private-IP Workbench instance in a custom VPC.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
        network_id: The ID of the VPC network in the project.
        subnet_id: The ID of the subnetwork in the same region.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    region_id = "-".join(location_id.split("-")[:-1])
    network = f"projects/{project_id}/global/networks/{network_id}"
    subnet = (
        f"projects/{project_id}/regions/{region_id}/subnetworks/{subnet_id}"
    )
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
        response = operation.result()
        print(f"Resource ID: {response.name}")
        print(f"Disable Public IP: {response.gce_setup.disable_public_ip}")
        print(f"State: {response.state.name}")
    except exceptions.AlreadyExists as err:
        print(
            f"error: Instance '{instance_id}' already exists in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_create_instance_private_vpc]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a private-IP Workbench instance in a custom VPC."
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="The Google Cloud project ID.",
    )
    parser.add_argument(
        "--location-id",
        default="us-central1-a",
        help="The Compute Engine zone.",
    )
    parser.add_argument(
        "--instance-id",
        default="example-private-instance",
        help="The ID for the new Workbench instance.",
    )
    parser.add_argument(
        "--network-id",
        default="example-network",
        help="The VPC network ID.",
    )
    parser.add_argument(
        "--subnet-id",
        default="example-subnet",
        help="The subnetwork ID.",
    )
    args = parser.parse_args()
    create_instance_private_vpc(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
        network_id=args.network_id,
        subnet_id=args.subnet_id,
    )
