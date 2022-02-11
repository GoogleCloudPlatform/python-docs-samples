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
# [START compute_preemptible_history]
import datetime

# [END compute_preemptible_history]
# [START compute_preemptible_create]
import sys

# [END compute_preemptible_create]

# [START compute_preemptible_history]
from typing import List, Tuple

# [END compute_preemptible_history]

# [START compute_preemptible_create]
# [START compute_preemptible_check]
# [START compute_preemptible_history]
from google.cloud import compute_v1

# [END compute_preemptible_history]
# [END compute_preemptible_check]
# [END compute_preemptible_create]

# [START compute_preemptible_history]
from google.cloud.compute_v1.services.zone_operations import pagers

# [END compute_preemptible_history]


# [START compute_preemptible_create]
def create_preemptible_instance(
    project_id: str, zone: str, instance_name: str,
) -> compute_v1.Instance:
    """
    Send an instance creation request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        instance_name: name of the new virtual machine.
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

    # Set the preemptible setting
    instance.scheduling = compute_v1.Scheduling()
    instance.scheduling.preemptible = True

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
    return instance_client.get(project=project_id, zone=zone, instance=instance_name)


# [END compute_preemptible_create]


# [START compute_preemptible_check]
def is_preemptible(project_id: str, zone: str, instance_name: str) -> bool:
    """
    Check if a given instance is preemptible or not.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        instance_name: name of the virtual machine to check.
    Returns:
        The preemptible status of the instance.
    """
    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(
        project=project_id, zone=zone, instance=instance_name
    )
    return instance.scheduling.preemptible


# [END compute_preemptible_check]


# [START compute_preemptible_history]
def list_zone_operations(
    project_id: str, zone: str, filter: str = ""
) -> pagers.ListPager:
    """
    List all recent operations the happened in given zone in a project. Optionally filter those
    operations by providing a filter. More about using the filter can be found here:
    https://cloud.google.com/compute/docs/reference/rest/v1/zoneOperations/list

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        instance_name: name of the virtual machine to look for.
    Returns:
        List of preemption operations in given zone.
    """
    operation_client = compute_v1.ZoneOperationsClient()
    request = compute_v1.ListZoneOperationsRequest()
    request.project = project_id
    request.zone = zone
    request.filter = filter

    return operation_client.list(request)


def preemption_history(
    project_id: str, zone: str, instance_name: str = None
) -> List[Tuple[str, datetime.datetime]]:
    """
    Get a list of preemption operations from given zone in a project. Optionally limit
    the results to instance name.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: "us-west3-b"
        instance_name: name of the virtual machine to look for.
    Returns:
        List of preemption operations in given zone.
    """
    if instance_name:
        filter = (
            f'operationType="compute.instances.preempted" '
            f"AND targetLink:instances/{instance_name}"
        )
    else:
        filter = 'operationType="compute.instances.preempted"'

    history = []

    for operation in list_zone_operations(project_id, zone, filter):
        this_instance_name = operation.target_link.rsplit("/", maxsplit=1)[1]
        if instance_name and this_instance_name == instance_name:
            # The filter used is not 100% accurate, it's `contains` not `equals`
            # So we need to check the name to make sure it's the one we want.
            moment = datetime.datetime.fromisoformat(operation.insert_time)
            history.append((instance_name, moment))

    return history


# [END compute_preemptible_history]
