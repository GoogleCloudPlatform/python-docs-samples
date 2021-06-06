#!/usr/bin/env python

# Copyright 2021 Google LLC
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
"""
A sample script showing how to create, list and delete Google Compute Engine
instances using the google-cloud-compute library. It can be run from command
line to create, list and delete an instance in a given project in a given zone.
"""

# [START compute_instances_create]
# [START compute_instances_delete]
import sys

# [START compute_instances_list]
# [START compute_instances_list_all]
# [START compute_instances_operation_check]
import typing

import google.cloud.compute_v1 as compute_v1

# [END compute_instances_operation_check]
# [END compute_instances_list_all]
# [END compute_instances_list]
# [END compute_instances_delete]
# [END compute_instances_create]


# [START compute_instances_list]
def list_instances(project_id: str, zone: str) -> typing.Iterable[compute_v1.Instance]:
    """
    Gets a list of instances created in given project in given zone.
    Returns an iterable collection of Instance objects.

    Args:
        project_id: ID or number of the project you want to use.
        zone: Name of the zone you want to check, for example: us-west3-b

    Returns:
        An iterable collection of Instance objects.
    """
    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project_id, zone=zone)

    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")

    return instance_list


# [END compute_instances_list]

# [START compute_instances_list_all]
def list_all_instances(
    project_id: str,
) -> typing.Dict[str, typing.Iterable[compute_v1.Instance]]:
    """
    Returns a dictionary of all instances present in a project, grouped by their zone.

    Args:
        project_id: ID or number of the project you want to use.

    Returns:
        A dictionary with zone names as keys (in form of "zones/{zone_name}") and
        iterable collections of Instance objects as values.
    """
    instance_client = compute_v1.InstancesClient()
    agg_list = instance_client.aggregated_list(project=project_id)
    all_instances = {}
    print("Instances found:")
    for zone, response in agg_list:
        if response.instances:
            all_instances[zone] = response.instances
            print(f" {zone}:")
            for instance in response.instances:
                print(f" - {instance.name} ({instance.machine_type})")
    return all_instances


# [END compute_instances_list_all]


# [START compute_instances_create]
def create_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    machine_type: str = "n1-standard-1",
    source_image: str = "projects/debian-cloud/global/images/family/debian-10",
    network_name: str = "global/networks/default",
) -> compute_v1.Instance:
    """
    Sends an instance creation request to GCP and waits for it to complete.

    Args:
        project_id: ID or number of the project you want to use.
        zone: Name of the zone you want to use, for example: us-west3-b
        instance_name: Name of the new machine.
        machine_type: Machine type you want to create in following format:
            "zones/{zone}/machineTypes/{type_name}". For example:
            "zones/europe-west3-c/machineTypes/f1-micro"
            You can find the list of available machine types using:
            https://cloud.google.com/sdk/gcloud/reference/compute/machine-types/list
        source_image: Path the the disk image you want to use for your boot
            disk. This can be one of the public images
            (e.g. "projects/debian-cloud/global/images/family/debian-10")
            or a private image you have access to.
            You can check the list of available public images using:
            $ gcloud compute images list
        network_name: Name of the network you want the new instance to use.
            For example: global/networks/default - if you want to use the
            default network.

    Returns:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()

    # Every machine requires at least one persistent disk
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        source_image  # "projects/debian-cloud/global/images/family/debian-10"
    )
    initialize_params.disk_size_gb = "10"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True
    disk.type_ = compute_v1.AttachedDisk.Type.PERSISTENT

    # Every machine needs to be connected to a VPC network.
    # The 'default' network is created automatically in every project.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = network_name

    # Collecting all the information into the Instance object
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.disks = [disk]
    full_machine_type_name = f"zones/{zone}/machineTypes/{machine_type}"
    instance.machine_type = full_machine_type_name
    instance.network_interfaces = [network_interface]

    # Preparing the InsertInstanceRequest
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    print(f"Creating the {instance_name} instance in {zone}...")
    operation = instance_client.insert(request=request)
    if operation.status == compute_v1.Operation.Status.RUNNING:
        operation_client = compute_v1.ZoneOperationsClient()
        operation = operation_client.wait(
            operation=operation.name, zone=zone, project=project_id
        )
    if operation.error:
        print("Error during creation:", operation.error, file=sys.stderr)
    if operation.warnings:
        print("Warning during creation:", operation.warnings, file=sys.stderr)
    print(f"Instance {instance_name} created.")
    return instance


# [END compute_instances_create]


# [START compute_instances_delete]
def delete_instance(project_id: str, zone: str, machine_name: str) -> None:
    """
    Sends a delete request to GCP and waits for it to complete.

    Args:
        project_id: ID or number of the project you want to use.
        zone: Name of the zone you want to use, for example: us-west3-b
        machine_name: Name of the machine you want to delete.
    """
    instance_client = compute_v1.InstancesClient()

    print(f"Deleting {machine_name} from {zone}...")
    operation = instance_client.delete(
        project=project_id, zone=zone, instance=machine_name
    )
    if operation.status == compute_v1.Operation.Status.RUNNING:
        operation_client = compute_v1.ZoneOperationsClient()
        operation = operation_client.wait(
            operation=operation.name, zone=zone, project=project_id
        )
    if operation.error:
        print("Error during deletion:", operation.error, file=sys.stderr)
    if operation.warnings:
        print("Warning during deletion:", operation.warnings, file=sys.stderr)
    print(f"Instance {machine_name} deleted.")
    return


# [END compute_instances_delete]


# [START compute_instances_operation_check]
def wait_for_operation(
    operation: compute_v1.Operation, project_id: str
) -> compute_v1.Operation:
    """
    This method waits for an operation to be completed. Calling this function
    will block until the operation is finished.

    Args:
        operation: The Operation object representing the operation you want to
            wait on.
        project_id: ID or number of the project owning the operation.

    Returns:
        Finished Operation object.
    """
    kwargs = {"project": project_id, "operation": operation.name}
    if operation.zone:
        client = compute_v1.ZoneOperationsClient()
        # Operation.zone is a full URL address of a zone, so we need to extract just the name
        kwargs["zone"] = operation.zone.rsplit("/", maxsplit=1)[1]
    elif operation.region:
        client = compute_v1.RegionOperationsClient()
        # Operation.region is a full URL address of a zone, so we need to extract just the name
        kwargs["region"] = operation.region.rsplit("/", maxsplit=1)[1]
    else:
        client = compute_v1.GlobalOperationsClient()
    return client.wait(**kwargs)


# [END compute_instances_operation_check]


def main(project_id: str, zone: str, instance_name: str) -> None:

    create_instance(project_id, zone, instance_name)

    zone_instances = list_instances(project_id, zone)
    print(f"Instances found in {zone}:", ", ".join(i.name for i in zone_instances))

    all_instances = list_all_instances(project_id)
    print(f"Instances found in project {project_id}:")
    for i_zone, instances in all_instances.items():
        print(f"{i_zone}:", ", ".join(i.name for i in instances))

    delete_instance(project_id, zone, instance_name)


if __name__ == "__main__":
    import uuid
    import google.auth
    import google.auth.exceptions

    try:
        default_project_id = google.auth.default()[1]
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        instance_name = "quickstart-" + uuid.uuid4().hex[:10]
        instance_zone = "europe-central2-b"
        main(default_project_id, instance_zone, instance_name)
