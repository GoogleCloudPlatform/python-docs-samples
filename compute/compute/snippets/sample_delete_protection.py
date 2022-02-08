#  Copyright 2022 Google LLC
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
# [START compute_delete_protection_create]
import sys

# [END compute_delete_protection_create]

# [START compute_delete_protection_get]
# [START compute_delete_protection_set]
# [START compute_delete_protection_create]
from google.cloud import compute_v1

# [END compute_delete_protection_create]
# [END compute_delete_protection_set]
# [END compute_delete_protection_get]


# [START compute_delete_protection_create]
def create_instance(
    project_id: str, zone: str, instance_name: str, delete_protection: bool,
) -> compute_v1.Instance:
    """
    Send an instance creation request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the new virtual machine.
        delete_protection: boolean value indicating if the new virtual machine should be
            protected against deletion or not.
    Returns:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    # Describe the size and source image of the boot disk to attach to the instance.
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-10"
    )
    initialize_params.disk_size_gb = 10
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True
    disk.type_ = "PERSISTENT"

    # Use the default VPC network.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "default"

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.disks = [disk]
    instance.machine_type = f"zones/{zone}/machineTypes/e2-small"
    instance.network_interfaces = [network_interface]

    # Set the delete protection bit
    instance.deletion_protection = delete_protection

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    # Wait for the create operation to complete.
    print(f"Creating the {instance_name} instance in {zone}...")
    operation = instance_client.insert_unary(request=request)
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, zone=zone, project=project_id
        )
    if operation.error:
        print("Error during creation:", operation.error, file=sys.stderr)
    if operation.warnings:
        print("Warning during creation:", operation.warnings, file=sys.stderr)
    print(f"Instance {instance_name} created.")
    return instance


# [END compute_delete_protection_create]


# [START compute_delete_protection_set]
def set_delete_protection(
    project_id: str, zone: str, instance_name: str, delete_protection: bool
):
    """
    Updates the delete protection setting of given instance.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the virtual machine to update.
        delete_protection: boolean value indicating if the virtual machine should be
            protected against deletion or not.
    """
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    request = compute_v1.SetDeletionProtectionInstanceRequest()
    request.project = project_id
    request.zone = zone
    request.resource = instance_name
    request.deletion_protection = delete_protection

    operation = instance_client.set_deletion_protection_unary(request)
    operation_client.wait(project=project_id, zone=zone, operation=operation.name)


# [END compute_delete_protection_set]


# [START compute_delete_protection_get]
def get_delete_protection(project_id: str, zone: str, instance_name: str) -> bool:
    """
    Returns the state of delete protection flag of given instance.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the virtual machine to check.
    Returns:
        The state of the delete protection setting.
    """
    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(
        project=project_id, zone=zone, instance=instance_name
    )
    return instance.deletion_protection


# [END compute_delete_protection_get]
