# Copyright 2015 Google, Inc.
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

from google.cloud import dns
from google.cloud.exceptions import NotFound

import pytest

import main

PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
TEST_ZONE_NAME = 'test-zone' + str(uuid.uuid4())
TEST_ZONE_DNS_NAME = 'theadora.is.'
TEST_ZONE_DESCRIPTION = 'Test zone'


def delay_rerun(*args):
    time.sleep(5)
    return True


@pytest.fixture
def client():
    client = dns.Client(PROJECT)

    yield client

    # Delete anything created during the test.
    for zone in client.list_zones():
        try:
            zone.delete()
        except NotFound:  # May have been in process
            pass


@pytest.fixture
def zone(client):
    zone = client.zone(TEST_ZONE_NAME, TEST_ZONE_DNS_NAME)
    zone.description = TEST_ZONE_DESCRIPTION
    zone.create()

    yield zone

    if zone.exists():
        try:
            zone.delete()
        except NotFound:  # May have been under way
            pass


@pytest.mark.flaky
def test_create_zone(client):
    zone = main.create_zone(
        PROJECT,
        TEST_ZONE_NAME,
        TEST_ZONE_DNS_NAME,
        TEST_ZONE_DESCRIPTION)

    assert zone.name == TEST_ZONE_NAME
    assert zone.dns_name == TEST_ZONE_DNS_NAME
    assert zone.description == TEST_ZONE_DESCRIPTION


@pytest.mark.flaky(max_runs=3, min_passes=1, rerun_filter=delay_rerun)
def test_get_zone(client, zone):
    zone = main.get_zone(PROJECT, TEST_ZONE_NAME)

    assert zone.name == TEST_ZONE_NAME
    assert zone.dns_name == TEST_ZONE_DNS_NAME
    assert zone.description == TEST_ZONE_DESCRIPTION


@pytest.mark.flaky(max_runs=3, min_passes=1, rerun_filter=delay_rerun)
def test_list_zones(client, zone):
    zones = main.list_zones(PROJECT)

    assert TEST_ZONE_NAME in zones


@pytest.mark.flaky(max_runs=3, min_passes=1, rerun_filter=delay_rerun)
def test_list_resource_records(client, zone):
    records = main.list_resource_records(PROJECT, TEST_ZONE_NAME)

    assert records


@pytest.mark.flaky(max_runs=3, min_passes=1, rerun_filter=delay_rerun)
def test_list_changes(client, zone):
    changes = main.list_changes(PROJECT, TEST_ZONE_NAME)

    assert changes


@pytest.mark.flaky(max_runs=3, min_passes=1, rerun_filter=delay_rerun)
def test_delete_zone(client, zone):
    main.delete_zone(PROJECT, TEST_ZONE_NAME)
