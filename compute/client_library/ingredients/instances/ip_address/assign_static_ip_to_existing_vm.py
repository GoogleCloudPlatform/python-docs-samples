#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa


import uuid

from google.cloud.compute_v1 import InstancesClient
from google.cloud.compute_v1.types import (
    AccessConfig,
    AddAccessConfigInstanceRequest,
    DeleteAccessConfigInstanceRequest,
)


# <INGREDIENT assign_static_ip_to_existing_vm>
def assign_static_ip_to_existing_vm(
    project_id: str,
    zone: str,
    instance_name: str,
    ip_address: str,
    network_interface_name: str = "nic0",
):
    """
    Updates or creates an access configuration for a VM instance to assign a static external IP.
    As network interface is immutable - deletion stage is required in case of any assigned ip (static or ephemeral).
    VM and ip address must be created before calling this function.
    IMPORTANT: VM and assigned IP must be in the same region.

    Args:
        project_id (str): Project ID.
        zone (str): Zone where the VM is located.
        instance_name (str): Name of the VM instance.
        ip_address (str): New static external IP address to assign to the VM.
        network_interface_name (str): Name of the network interface to assign.

    Returns:
        google.cloud.compute_v1.types.Instance: Updated instance object.
    """
    client = InstancesClient()
    instance = client.get(project=project_id, zone=zone, instance=instance_name)
    network_interface = next(
        (ni for ni in instance.network_interfaces if ni.name == network_interface_name),
        None,
    )

    if network_interface is None:
        raise ValueError(
            f"No network interface named '{network_interface_name}' found on instance {instance_name}."
        )

    access_config = next(
        (ac for ac in network_interface.access_configs if ac.type_ == "ONE_TO_ONE_NAT"),
        None,
    )

    if access_config:
        # Delete the existing access configuration first
        delete_request = DeleteAccessConfigInstanceRequest(
            project=project_id,
            zone=zone,
            instance=instance_name,
            access_config=access_config.name,
            network_interface=network_interface_name,
            request_id=str(uuid.uuid4()),
        )
        delete_operation = client.delete_access_config(delete_request)
        delete_operation.result()

    # Add a new access configuration with the new IP
    add_request = AddAccessConfigInstanceRequest(
        project=project_id,
        zone=zone,
        instance=instance_name,
        network_interface="nic0",
        access_config_resource=AccessConfig(
            nat_i_p=ip_address, type_="ONE_TO_ONE_NAT", name="external-nat"
        ),
        request_id=str(uuid.uuid4()),
    )
    add_operation = client.add_access_config(add_request)
    add_operation.result()

    updated_instance = client.get(project=project_id, zone=zone, instance=instance_name)
    return updated_instance


# </INGREDIENT>
