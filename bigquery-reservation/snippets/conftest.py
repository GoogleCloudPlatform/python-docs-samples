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

import datetime
import os
import time

from google.cloud.bigquery_reservation_v1.services import reservation_service
from google.cloud.bigquery_reservation_v1.types import reservation as reservation_types
import pytest


@pytest.fixture(scope="session")
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="session")
def reservation_client() -> reservation_service.ReservationServiceClient:
    return reservation_service.ReservationServiceClient()


@pytest.fixture(scope="session")
def location() -> str:
    return "US"


@pytest.fixture(scope="session")
def location_path(project_id: str, location: str) -> str:
    return reservation_service.ReservationServiceClient.common_location_path(
        project_id, location
    )


@pytest.fixture(scope="session", autouse=True)
def capacity_commitment(location_path: str, reservation_client: reservation_service.ReservationServiceClient) -> reservation_types.CapacityCommitment:
    # TODO(b/196082966): If custom names or creation date property are added,
    # do pre-test cleanup of past commitments.
    commitment = reservation_types.CapacityCommitment()
    commitment.slot_count = 100
    commitment.plan = reservation_types.CapacityCommitment.CommitmentPlan.FLEX
    commitment = reservation_client.create_capacity_commitment(parent=location_path, capacity_commitment=commitment)
    yield commitment
    # Commitments can only be removed after 1 minute.
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = commitment.commitment_end_time - now
    sleep_seconds = max(0, delta.total_seconds()) + 5
    time.sleep(sleep_seconds)
    reservation_client.delete_capacity_commitment(name=commitment.name)
