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

import argparse
# [START compute_instances_list]
# [START compute_instances_create]
# [START compute_instances_delete]
# [START compute_instances_check]
import typing
import google.cloud.compute_v1 as gce
# [END compute_instances_check]
# [END compute_instances_delete]
# [END compute_instances_create]
# [END compute_instances_list]


# [START compute_instances_list]
def list_instances(project: str, zone: str) -> typing.Iterable[gce.Instance]:
    """
    Gets a list of instances created in given project in given zone.
    Returns an iterable collection of Instance objects.

    Args:
        project: Name of the project you want to use.
        zone: Name of the zone you want to check, for example: us-west3-b

    Returns:
        An iterable collection of Instance objects.
    """
    instance_client = gce.InstancesClient()
    instance_list = instance_client.list(project=project, zone=zone)
    return instance_list


def list_all_instances(project: str) -> typing.Dict[str, typing.Iterable[gce.Instance]]:
    """
    Returns a dictionary of all instances present in a project, grouped by their zone.

    Args:
        project: Name of the project you want to use.

    Returns:
        A dictionary with zone names as keys (in form of "zones/{zone_name}") and
        iterable collections of Instance objects as values.
    """
    instance_client = gce.InstancesClient()
    agg_list = instance_client.aggregated_list(project=project)
    all_instances = {}
    for zone, response in agg_list:
        if response.instances:
            all_instances[zone] = response.instances
    return all_instances
# [END compute_instances_list]


# [START compute_instances_create]
def create_instance(project: str, zone: str, machine_type: str,
                    machine_name: str, source_image: str) -> gce.Instance:
    """
    Sends an instance creation request to GCP and waits for it to complete.

    Args:
        project: Name of the project you want to use.
        zone: Name of the zone you want to use, for example: us-west3-b
        machine_type: Machine type you want to create in following format:
            "zones/{zone}/machineTypes/{type_name}". For example:
            "zones/europe-west3-c/machineTypes/f1-micro"
        machine_name: Name of the new machine.
        source_image: Path the the disk image you want to use for your boot
            disk. This can be one of the public images
            (e.g. "projects/debian-cloud/global/images/family/debian-10")
            or a private image you have access to.

    Returns:
        Instance object.
    """
    instance_client = gce.InstancesClient()

    # Every machine requires at least one persistent disk
    disk = gce.AttachedDisk()
    initialize_params = gce.AttachedDiskInitializeParams()
    initialize_params.source_image = source_image  # "projects/debian-cloud/global/images/family/debian-10"
    initialize_params.disk_size_gb = "10"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True
    disk.type_ = gce.AttachedDisk.Type.PERSISTENT

    # Every machine needs to be connected to a VPC network.
    # The 'default' network is created automatically in every project.
    network_interface = gce.NetworkInterface()
    network_interface.name = "default"

    # Collecting all the information into the Instance object
    instance = gce.Instance()
    instance.name = machine_name
    instance.disks = [disk]
    instance.machine_type = machine_type  # "zones/europe-central2-a/machineTypes/n1-standard-8"
    instance.network_interfaces = [network_interface]

    # Preparing the InsertInstanceRequest
    request = gce.InsertInstanceRequest()
    request.zone = zone  # "europe-central2-a"
    request.project = project  # "diregapic-mestiv"
    request.instance_resource = instance

    print(f"Creating the {machine_name} instance in {zone}...")
    operation = instance_client.insert(request=request)
    # wait_result = operation_client.wait(operation=operation.name, zone=zone, project=project)
    operation = wait_for_operation(operation, project)
    if operation.error:
        pass
    if operation.warnings:
        pass
    print(f"Instance {machine_name} created.")
    return instance
# [END compute_instances_create]


# [START compute_instances_delete]
def delete_instance(project: str, zone: str, machine_name: str) -> None:
    """
    Sends a delete request to GCP and waits for it to complete.

    Args:
        project: Name of the project you want to use.
        zone: Name of the zone you want to use, for example: us-west3-b
        machine_name: Name of the machine you want to delete.
    """
    instance_client = gce.InstancesClient()

    print(f"Deleting {machine_name} from {zone}...")
    operation = instance_client.delete(project=project, zone=zone, instance=machine_name)
    operation = wait_for_operation(operation, project)
    if operation.error:
        pass
    if operation.warnings:
        pass
    print(f"Instance {machine_name} deleted.")
    return
# [END compute_instances_delete]


# [START compute_instances_check]
def wait_for_operation(operation: gce.Operation, project: str) -> gce.Operation:
    """
    This method waits for an operation to be completed. Calling this function
    will block until the operation is finished.

    Args:
        operation: The Operation object representing the operation you want to
            wait on.
        project: Name of the project owning the operation.

    Returns:
        Finished Operation object.
    """
    kwargs = {'project': project, 'operation': operation.name}
    if operation.zone:
        client = gce.ZoneOperationsClient()
        # Operation.zone is a full URL address of a zone, so we need to extract just the name
        kwargs['zone'] = operation.zone.rsplit('/', maxsplit=1)[1]
    elif operation.region:
        client = gce.RegionOperationsClient()
        # Operation.region is a full URL address of a zone, so we need to extract just the name
        kwargs['region'] = operation.region.rsplit('/', maxsplit=1)[1]
    else:
        client = gce.GlobalOperationsClient()
    print(kwargs)
    return client.wait(**kwargs)
# [END compute_instances_check]


def main(project, zone, machine_name):
    # You can find the list of available machine types using:
    # https://cloud.google.com/sdk/gcloud/reference/compute/machine-types/list
    machine_type = f"zones/{zone}/machineTypes/f1-micro"
    # You can check the list of available public images using:
    # gcloud compute images list
    source_image = "projects/debian-cloud/global/images/family/debian-10"

    create_instance(project, zone, machine_type, machine_name, source_image)

    zone_instances = list_instances(project, zone)
    print(f"Instances found in {zone}: ", ", ".join(i.name for i in zone_instances))

    all_instances = list_all_instances(project)
    print(f"Instances found in project: ")
    for i_zone, instances in all_instances.items():
        print(f"{i_zone}: ", ", ".join(i.name for i in instances))

    delete_instance(project, zone, machine_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("zone", help="Google Cloud zone name")
    parser.add_argument("machine_name", help="Name for the demo machine")

    args = parser.parse_args()

    main(args.project_id, args.zone, args.machine_name)
