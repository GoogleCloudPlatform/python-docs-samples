# Copyright 2015, Google, Inc.
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

from gcp.testing.flaky import flaky
from google.cloud import dns
import pytest

import main

TEST_ZONE_NAME = 'test-zone'
TEST_ZONE_DNS_NAME = 'theadora.is.'
TEST_ZONE_DESCRIPTION = 'Test zone'


@pytest.yield_fixture
def client(cloud_config):
    client = dns.Client(cloud_config.project)

    yield client

    # Delete anything created during the test.
    for zone in client.list_zones():
        zone.delete()


@pytest.yield_fixture
def zone(client, cloud_config):
    zone = client.zone(TEST_ZONE_NAME, TEST_ZONE_DNS_NAME)
    zone.description = TEST_ZONE_DESCRIPTION
    zone.create()

    yield zone

    if zone.exists():
        zone.delete()


@flaky
def test_create_zone(client, cloud_config):
    zone = main.create_zone(
        cloud_config.project,
        TEST_ZONE_NAME,
        TEST_ZONE_DNS_NAME,
        TEST_ZONE_DESCRIPTION)

    assert zone.name == TEST_ZONE_NAME
    assert zone.dns_name == TEST_ZONE_DNS_NAME
    assert zone.description == TEST_ZONE_DESCRIPTION


@flaky
def test_get_zone(client, cloud_config, zone):
    zone = main.get_zone(cloud_config.project, TEST_ZONE_NAME)

    assert zone.name == TEST_ZONE_NAME
    assert zone.dns_name == TEST_ZONE_DNS_NAME
    assert zone.description == TEST_ZONE_DESCRIPTION


@flaky
def test_list_zones(client, cloud_config, zone):
    zones = main.list_zones(cloud_config.project)

    assert TEST_ZONE_NAME in zones


@flaky
def test_delete_zone(client, cloud_config, zone):
    main.delete_zone(cloud_config.project, TEST_ZONE_NAME)


@flaky
def test_list_resource_records(client, cloud_config, zone):
    records = main.list_resource_records(cloud_config.project, TEST_ZONE_NAME)

    assert records


@flaky
def test_list_changes(client, cloud_config, zone):
    changes = main.list_changes(cloud_config.project, TEST_ZONE_NAME)

    assert changes
