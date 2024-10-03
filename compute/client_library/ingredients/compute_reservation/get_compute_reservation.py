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
from google.cloud.compute_v1.types import compute


# <INGREDIENT get_compute_reservation>
def get_compute_reservation(
    project_id: str,
    zone: str = "us-central1-a",
    reservation_name="your-reservation-name",
) -> compute.Reservation:
    """
    Retrieves a compute reservation from GCP.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone of the reservation.
        reservation_name (str): The name of the reservation to retrieve.
    Returns:
        compute.Reservation: The reservation object retrieved from Google Cloud.
    """

    client = compute_v1.ReservationsClient()

    reservation = client.get(
        project=project_id,
        zone=zone,
        reservation=reservation_name,
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
