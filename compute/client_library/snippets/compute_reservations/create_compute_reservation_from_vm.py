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

# THIS IS A DRAFT FILE AND SHOULD NOT BE USED IN PRODUCTION

from google.cloud import compute_v1


def create_compute_reservation_from_vm(
    project_id: str,
    zone: str = "us-central1-a",
    reservation_name="your-reservation-name",
    vm_name="your-vm-name",
) -> compute_v1.Reservation:
    """Creates a compute reservation in GCP.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone to create the reservation.
        reservation_name (str): The name of the reservation to create.
    Returns:
        Reservation object that represents the new reservation.
    """
    instance_client = compute_v1.InstancesClient()

    existing_vm = instance_client.get(project=project_id, zone=zone, instance=vm_name)

    accelerators = existing_vm.guest_accelerators

    guest_accelerators = [
        compute_v1.AcceleratorConfig(
            accelerator_count=a.accelerator_count,
            accelerator_type=a.accelerator_type.split("/")[-1],
        )
        for a in accelerators
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

    client.insert(
        project=project_id,
        zone=zone,
        reservation_resource=reservation,
    )

    reservation = client.get(
        project=project_id, zone=zone, reservation=reservation_name
    )

    print("Name: ", reservation.name)
    print("STATUS: ", reservation.status)
    print(reservation.specific_reservation)

    return reservation


if __name__ == "__main__":
    create_compute_reservation_from_vm(
        "11",
        "us-central1-f",
        "reservation-name",
        "instance-20241001-141510",
    )
