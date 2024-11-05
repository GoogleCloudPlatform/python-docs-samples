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


# <INGREDIENT create_compute_reservation>
def create_compute_reservation(
    project_id: str,
    zone: str = "us-central1-a",
    reservation_name="your-reservation-name",
) -> compute_v1.Reservation:
    """Creates a compute reservation in GCP.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone to create the reservation.
        reservation_name (str): The name of the reservation to create.
    Returns:
        Reservation object that represents the new reservation.
    """

    instance_properties = compute_v1.AllocationSpecificSKUAllocationReservedInstanceProperties(
        machine_type="n1-standard-1",
        # Optional. Specifies the minimum CPU platform for the VM instance.
        min_cpu_platform="Intel Ivy Bridge",
        # Optional. Specifies amount of local ssd to reserve with each instance.
        local_ssds=[
            compute_v1.AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk(
                disk_size_gb=375, interface="NVME"
            ),
            compute_v1.AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk(
                disk_size_gb=375, interface="SCSI"
            ),
        ],
        # Optional. Specifies the GPUs allocated to each instance.
        # guest_accelerators=[
        #     compute_v1.AcceleratorConfig(
        #         accelerator_count=1, accelerator_type="nvidia-tesla-t4"
        #     )
        # ],
    )

    reservation = compute_v1.Reservation(
        name=reservation_name,
        specific_reservation=compute_v1.AllocationSpecificSKUReservation(
            count=3,  # Number of resources that are allocated.
            # If you use source_instance_template, you must exclude the instance_properties field.
            # It can be a full or partial URL.
            # source_instance_template="projects/[PROJECT_ID]/global/instanceTemplates/my-instance-template",
            instance_properties=instance_properties,
        ),
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
    #   machine_type: "n1-standard-1"
    #   local_ssds {
    #     disk_size_gb: 375
    #     interface: "NVME"
    #   }
    # ...

    return reservation


# </INGREDIENT>
