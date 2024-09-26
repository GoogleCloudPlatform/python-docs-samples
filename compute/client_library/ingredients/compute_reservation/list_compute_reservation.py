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
from google.cloud.compute_v1.services.reservations.pagers import ListPager


# <INGREDIENT list_compute_reservation>
def list_compute_reservation(project_id: str, zone: str = "us-central1-a") -> ListPager:
    """
    Lists all compute reservations in a specified Google Cloud project and zone.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone of the reservations.
    Returns:
        ListPager: A pager object containing the list of reservations.
    """

    client = compute_v1.ReservationsClient()

    reservations_list = client.list(
        project=project_id,
        zone=zone,
    )

    for reservation in reservations_list:
        print("Name: ", reservation.name)
        print(
            "Machine type: ",
            reservation.specific_reservation.instance_properties.machine_type,
        )
    # Example response:
    # Name:  my-reservation_1
    # Machine type:  n1-standard-1
    # Name:  my-reservation_2
    # Machine type:  n1-standard-1

    return reservations_list


# </INGREDIENT>
