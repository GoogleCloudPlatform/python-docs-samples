# Copyright 2020 Google LLC
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

# [START bigqueryreservation_quickstart]
import argparse

from google.cloud import bigquery_reservation_v1


def main(
    project_id: str = "your-project-id", location: str = "US", transport: str = "grpc"
) -> None:
    # Constructs the client for interacting with the service.
    client = bigquery_reservation_v1.ReservationServiceClient(transport=transport)

    report_reservations(client, project_id, location)


def report_reservations(
    client: bigquery_reservation_v1.ReservationServiceClient,
    project_id: str,
    location: str,
) -> None:
    """Prints details and summary information about reservations defined within
    a given admin project and location.
    """
    print("Reservations in project {} in location {}".format(project_id, location))
    req = bigquery_reservation_v1.ListReservationsRequest(
        parent=client.common_location_path(project_id, location)
    )
    total_reservations = 0
    for reservation in client.list_reservations(request=req):
        print(
            f"\tReservation {reservation.name} "
            f"has {reservation.slot_capacity} slot capacity."
        )
        total_reservations = total_reservations + 1
    print(f"\n{total_reservations} reservations processed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str)
    parser.add_argument("--location", default="US", type=str)
    args = parser.parse_args()
    main(project_id=args.project_id, location=args.location)

# [END bigqueryreservation_quickstart]
