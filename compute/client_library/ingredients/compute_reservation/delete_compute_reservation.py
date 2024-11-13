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

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


# <INGREDIENT delete_compute_reservation>
def delete_compute_reservation(
    project_id: str,
    zone: str = "us-central1-a",
    reservation_name="your-reservation-name",
) -> ExtendedOperation:
    """
    Deletes a compute reservation in Google Cloud.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone of the reservation.
        reservation_name (str): The name of the reservation to delete.
    Returns:
        The operation response from the reservation deletion request.
    """

    client = compute_v1.ReservationsClient()

    operation = client.delete(
        project=project_id,
        zone=zone,
        reservation=reservation_name,
    )

    wait_for_extended_operation(operation, "Reservation deletion")
    print(operation.status)
    # Example response:
    # Status.DONE
    return operation


# </INGREDIENT>
