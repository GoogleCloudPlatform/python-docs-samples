#  Copyright 2024 Google LLC
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

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT create_reservation_from_template>
def create_reservation_from_template(
    project_id: str, reservation_name: str, template: str
) -> compute_v1.Reservation:
    """
    Create a new reservation based on an existing template.

    Args:
        project_id: project ID or project number of the Cloud project you use.
        reservation_name: the name of new reservation.
        template: existing template path. Following formats are allowed:
            - projects/{project_id}/global/instanceTemplates/{template_name}
            - projects/{project_id}/regions/{region}/instanceTemplates/{template_name}
            - https://www.googleapis.com/compute/v1/projects/{project_id}/global/instanceTemplates/instanceTemplate
            - https://www.googleapis.com/compute/v1/projects/{project_id}/regions/{region}/instanceTemplates/instanceTemplate

    Returns:
        Reservation object that represents the new reservation.
    """

    reservations_client = compute_v1.ReservationsClient()
    request = compute_v1.InsertReservationRequest()
    request.project = project_id
    request.zone = "us-central1-a"

    specific_reservation = compute_v1.AllocationSpecificSKUReservation()
    specific_reservation.count = 1
    specific_reservation.source_instance_template = template

    reservation = compute_v1.Reservation()
    reservation.name = reservation_name
    reservation.specific_reservation = specific_reservation

    request.reservation_resource = reservation
    operation = reservations_client.insert(request)
    wait_for_extended_operation(operation, "Reservation creation")

    return reservations_client.get(
        project=project_id, zone="us-central1-a", reservation=reservation_name
    )


# </INGREDIENT>
