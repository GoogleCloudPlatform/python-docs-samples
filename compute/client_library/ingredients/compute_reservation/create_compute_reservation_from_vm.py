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


# <INGREDIENT create_compute_reservation_from_vm>
def create_compute_reservation_from_vm(
    project_id: str,
    zone: str = "us-central1-a",
    reservation_name="your-reservation-name",
    vm_name="your-vm-name",
) -> compute_v1.Reservation:
    """Creates a compute reservation in GCP from an existing VM.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone of the VM. In this zone the reservation will be created.
        reservation_name (str): The name of the reservation to create.
        vm_name: The name of the VM to create the reservation from.
    Returns:
        Reservation object that represents the new reservation with the same properties as the VM.
    """
    instance_client = compute_v1.InstancesClient()
    existing_vm = instance_client.get(project=project_id, zone=zone, instance=vm_name)

    guest_accelerators = [
        compute_v1.AcceleratorConfig(
            accelerator_count=a.accelerator_count,
            accelerator_type=a.accelerator_type.split("/")[-1],
        )
        for a in existing_vm.guest_accelerators
    ]

    local_ssds = [
        compute_v1.AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk(
            disk_size_gb=disk.disk_size_gb, interface=disk.interface
        )
        for disk in existing_vm.disks
        if disk.disk_size_gb >= 375
    ]

    instance_properties = (
        compute_v1.AllocationSpecificSKUAllocationReservedInstanceProperties(
            machine_type=existing_vm.machine_type.split("/")[-1],
            min_cpu_platform=existing_vm.min_cpu_platform,
            local_ssds=local_ssds,
            guest_accelerators=guest_accelerators,
        )
    )

    reservation = compute_v1.Reservation(
        name=reservation_name,
        specific_reservation=compute_v1.AllocationSpecificSKUReservation(
            count=3,  # Number of resources that are allocated.
            instance_properties=instance_properties,
        ),
        specific_reservation_required=True,
    )

    # Create a client
    client = compute_v1.ReservationsClient()

    operation = client.insert(
        project=project_id,
        zone=zone,
        reservation_resource=reservation,
    )
    wait_for_extended_operation(operation, "Reservation creation")

    reservation = client.get(
        project=project_id, zone=zone, reservation=reservation_name
    )

    print("Name: ", reservation.name)
    print("STATUS: ", reservation.status)
    print(reservation.specific_reservation)
    # Example response:
    # Name:  your-reservation-name
    # STATUS:  READY
    # count: 3
    # instance_properties {
    #   machine_type: "n2-standard-2"
    #   local_ssds {
    #     disk_size_gb: 375
    #     interface: "SCSI"
    #   }
    # ...

    return reservation


# </INGREDIENT>
