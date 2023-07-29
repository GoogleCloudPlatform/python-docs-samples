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

import os

from google.cloud.bigquery_reservation_v1.services import reservation_service
import pytest


@pytest.fixture(scope="session")
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="session")
def reservation_client(
    transport: str = "grpc",
) -> reservation_service.ReservationServiceClient:
    return reservation_service.ReservationServiceClient(transport=transport)


@pytest.fixture(scope="session")
def location() -> str:
    return "US"


@pytest.fixture(scope="session")
def location_path(project_id: str, location: str) -> str:
    return reservation_service.ReservationServiceClient.common_location_path(
        project_id, location
    )
