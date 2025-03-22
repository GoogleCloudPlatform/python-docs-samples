# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import uuid

from google.cloud.dns import Client, ManagedZone
from google.cloud.exceptions import NotFound

import pytest

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TEST_ZONE_NAME_BASE = "test-zone"
TEST_ZONE_NAME_WITH_SUFFIX = TEST_ZONE_NAME_BASE + "-" + str(uuid.uuid4())
TEST_ZONE_DNS_NAME = "theadora.is."
TEST_ZONE_DESCRIPTION = "Test zone"


def delay_rerun() -> bool:
    time.sleep(5)
    return True


@pytest.fixture(scope="module")
def client() -> Client:
    client = Client(PROJECT_ID)

    yield client

    # Delete anything created during the test.
    for zone in client.list_zones():
        try:
            zone.delete()
        except NotFound:  # May have been in process
            pass


@pytest.fixture
def zone(client: Client) -> ManagedZone:
    zone_name = TEST_ZONE_NAME_BASE + "-" + str(uuid.uuid4())
    zone = client.zone(zone_name, TEST_ZONE_DNS_NAME)
    zone.description = TEST_ZONE_DESCRIPTION
    zone.create()

    yield zone

    if zone.exists():
        try:
            zone.delete()
        except NotFound:  # May have been in process
            pass


@pytest.fixture
def project_id() -> str:
    return PROJECT_ID


@pytest.fixture
def zone_name() -> str:
    return TEST_ZONE_NAME_WITH_SUFFIX


@pytest.fixture
def zone_dns_name() -> str:
    return TEST_ZONE_DNS_NAME


@pytest.fixture
def zone_description() -> str:
    return TEST_ZONE_DESCRIPTION
