# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def delete_reservation(
    project_id: str, location: str, reservation_id: str, transport: str
) -> None:
    original_project_id = project_id
    original_location = location
    original_reservation_id = reservation_id
    original_transport = transport

    # [START bigqueryreservation_reservation_delete]
    # TODO(developer): Set project_id to the project ID containing the
    # reservation.
    project_id = "your-project-id"

    # TODO(developer): Set location to the location of the reservation.
    # See: https://cloud.google.com/bigquery/docs/locations for a list of
    # available locations.
    location = "US"

    # TODO(developer): Set reservation_id to a unique ID of the reservation.
    reservation_id = "sample-reservation"

    # TODO(developer): Choose a transport to use. Either 'grpc' or 'rest'
    transport = "grpc"

    # [START_EXCLUDE]
    project_id = original_project_id
    location = original_location
    reservation_id = original_reservation_id
    transport = original_transport
    # [END_EXCLUDE]

    from google.cloud.bigquery_reservation_v1.services import reservation_service

    reservation_client = reservation_service.ReservationServiceClient(
        transport=transport
    )
    reservation_name = reservation_client.reservation_path(
        project_id, location, reservation_id
    )
    reservation_client.delete_reservation(name=reservation_name)

    print(f"Deleted reservation: {reservation_name}")
    # [END bigqueryreservation_reservation_delete]
