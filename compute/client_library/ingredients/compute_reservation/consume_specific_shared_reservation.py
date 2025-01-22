# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT consume_shared_project_reservation>
def consume_specific_shared_project_reservation(
    owner_project_id: str,
    shared_project_id: str,
    zone: str,
    reservation_name: str,
    instance_name: str,
    machine_type: str = "n1-standard-1",
    min_cpu_platform: str = "Intel Ivy Bridge",
) -> compute_v1.Instance:
    """
    Creates a specific reservation in a single project and launches a VM
    that consumes the newly created reservation.
    Args:
        owner_project_id (str): The ID of the Google Cloud project.
        shared_project_id: The ID of the owner project of the reservation in the same zone.
        zone (str): The zone to create the reservation.
        reservation_name (str): The name of the reservation to create.
        instance_name (str): The name of the instance to create.
        machine_type (str): The machine type for the instance.
        min_cpu_platform (str): The minimum CPU platform for the instance.
    """
    instance_properties = (
        compute_v1.AllocationSpecificSKUAllocationReservedInstanceProperties(
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
        )
    )

    reservation = compute_v1.Reservation(
        name=reservation_name,
        specific_reservation=compute_v1.AllocationSpecificSKUReservation(
            count=3,
            instance_properties=instance_properties,
        ),
        # Only VMs that target the reservation by name can consume from this reservation
        specific_reservation_required=True,
        share_settings=compute_v1.ShareSettings(
            share_type="SPECIFIC_PROJECTS",
            project_map={
                shared_project_id: compute_v1.ShareSettingsProjectConfig(
                    project_id=shared_project_id
                )
            },
        ),
    )

    # Create a reservation client
    client = compute_v1.ReservationsClient()
    operation = client.insert(
        project=owner_project_id,
        zone=zone,
        reservation_resource=reservation,
    )
    wait_for_extended_operation(operation, "Reservation creation")

    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"
    instance.min_cpu_platform = min_cpu_platform
    instance.zone = zone

    # Set the reservation affinity to target the specific reservation
    instance.reservation_affinity = compute_v1.ReservationAffinity(
        consume_reservation_type="SPECIFIC_RESERVATION",  # Type of reservation to consume
        key="compute.googleapis.com/reservation-name",
        # To consume this reservation from any consumer projects, specify the owner project of the reservation
        values=[f"projects/{owner_project_id}/reservations/{reservation_name}"],
    )
    # Define the disks for the instance
    instance.disks = [
        compute_v1.AttachedDisk(
            boot=True,  # Indicates that this is a boot disk
            auto_delete=True,  # The disk will be deleted when the instance is deleted
            initialize_params=compute_v1.AttachedDiskInitializeParams(
                source_image="projects/debian-cloud/global/images/family/debian-11",
                disk_size_gb=10,
            ),
        )
    ]
    instance.network_interfaces = [
        compute_v1.NetworkInterface(
            network="global/networks/default",  # The network to use
            access_configs=[
                compute_v1.AccessConfig(
                    name="External NAT",  # Name of the access configuration
                    type="ONE_TO_ONE_NAT",  # Type of access configuration
                )
            ],
        )
    ]
    # Create a request to insert the instance
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    # The instance will be created in the shared project
    request.project = shared_project_id
    request.instance_resource = instance

    vm_client = compute_v1.InstancesClient()
    operation = vm_client.insert(request)
    wait_for_extended_operation(operation, "instance creation")
    print(f"Instance {instance_name} from project {owner_project_id} created.")
    # The instance is created in the shared project, so we return it from there.
    return vm_client.get(project=shared_project_id, zone=zone, instance=instance_name)


# </INGREDIENT>
