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
from google.cloud.compute_v1.types import DeleteAccessConfigInstanceRequest


# <INGREDIENT unassign_static_ip_from_existing_vm>
def unassign_static_ip_from_existing_vm(
    project_id: str,
    zone: str,
    instance_name: str,
    network_interface_name: str = "nic0",
):
    """
    Updates access configuration for a VM instance to unassign a static external IP.
    VM (and IP address in case of static IP assigned) must be created before calling this function.

    Args:
        project_id (str): Project ID.
        zone (str): Zone where the VM is located.
        instance_name (str): Name of the VM instance.
        network_interface_name (str): Name of the network interface to unassign.
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
        # Delete the existing access configuration
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

    updated_instance = client.get(project=project_id, zone=zone, instance=instance_name)
    return updated_instance


# </INGREDIENT>
