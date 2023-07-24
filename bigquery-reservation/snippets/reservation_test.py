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

import google.api_core.exceptions
from google.cloud.bigquery_reservation_v1.services import reservation_service
import pytest
import test_utils.prefixer

from . import reservation_create, reservation_delete

# Reservation IDs are limited to 64 characters.
reservation_prefixer = test_utils.prefixer.Prefixer(
    "py-bq-r", "snippets", separator="-"
)


@pytest.fixture(scope="module", autouse=True)
def cleanup_reservations(
    reservation_client: reservation_service.ReservationServiceClient, location_path: str
) -> None:
    for reservation in reservation_client.list_reservations(parent=location_path):
        reservation_id = reservation.name.split("/")[-1]
        if reservation_prefixer.should_cleanup(reservation_id):
            reservation_client.delete_reservation(name=reservation.name)


@pytest.fixture(scope="session")
def reservation_id(
    reservation_client: reservation_service.ReservationServiceClient,
    project_id: str,
    location: str,
) -> str:
    id_ = reservation_prefixer.create_prefix()
    yield id_

    reservation_name = reservation_client.reservation_path(project_id, location, id_)
    try:
        reservation_client.delete_reservation(name=reservation_name)
    except google.api_core.exceptions.NotFound:
        pass


@pytest.mark.parametrize("transport", ["grpc", "rest"])
def test_reservation_samples(
    capsys: pytest.CaptureFixture,
    project_id: str,
    location: str,
    reservation_id: str,
    transport: str,
) -> None:
    slot_capacity = 100
    reservation = reservation_create.create_reservation(
        project_id, location, reservation_id, slot_capacity, transport
    )
    assert reservation.slot_capacity == 100
    assert reservation_id in reservation.name
    out, _ = capsys.readouterr()
    assert f"Created reservation: {reservation.name}" in out

    # The test for reservation_update is skipped for now, since without
    # capacity commitment we cannot decrease the capacity within one hour.

    # slot_capacity = 50
    # reservation = reservation_update.update_reservation(
    #     project_id, location, reservation_id, slot_capacity, transport
    # )
    # assert reservation.slot_capacity == 50
    # assert reservation_id in reservation.name
    # out, _ = capsys.readouterr()
    # assert f"Updated reservation: {reservation.name}" in out

    reservation_delete.delete_reservation(
        project_id, location, reservation_id, transport
    )
    out, _ = capsys.readouterr()
    assert "Deleted reservation" in out
    assert reservation_id in out
