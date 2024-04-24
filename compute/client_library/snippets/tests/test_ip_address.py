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

import uuid

import google.auth
from google.cloud.compute_v1 import AddressesClient, GlobalAddressesClient
from google.cloud.compute_v1.types import Address
import pytest

from ..instances.create_start_instance.create_from_public_image import (
    create_instance,
    disk_from_image,
    get_image_from_family,
)

from ..instances.delete import delete_instance
from ..instances.ip_address.get_static_ip_address import get_static_ip_address
from ..instances.ip_address.get_vm_address import get_instance_ip_address, IPType

PROJECT = google.auth.default()[1]
REGION = "us-central1"
INSTANCE_ZONE = "us-central1-b"


@pytest.fixture
def disk_fixture():
    project = "debian-cloud"
    family = "debian-10"
    disk_type = f"zones/{INSTANCE_ZONE}/diskTypes/pd-standard"
    newest_debian = get_image_from_family(project=project, family=family)
    # Create and return the disk configuration
    return [disk_from_image(disk_type, 10, True, newest_debian.self_link, True)]


@pytest.fixture
def instance_with_ips(disk_fixture):
    instance_name = "i" + uuid.uuid4().hex[:10]
    try:
        # Create the instance using the disk_fixture
        instance = create_instance(
            PROJECT, INSTANCE_ZONE, instance_name, disk_fixture, external_access=True
        )
        yield instance
    finally:
        # Cleanup after the test
        delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


@pytest.fixture
def static_ip(request):
    region = request.param["region"]
    address_name = f"ip-{uuid.uuid4()}"

    client_class = GlobalAddressesClient if region is None else AddressesClient
    client = client_class()

    # Create an IP address
    address = Address(
        name=address_name, address_type="EXTERNAL", network_tier="PREMIUM"
    )
    if region:
        address.region = region
        operation = client.insert(
            project=PROJECT, region=region, address_resource=address
        )
    else:
        operation = client.insert(project=PROJECT, address_resource=address)
    operation.result()

    yield address

    # Cleanup
    if region:
        operation = client.delete(project=PROJECT, region=region, address=address_name)
    else:
        operation = client.delete(project=PROJECT, address=address_name)
    operation.result()


@pytest.mark.parametrize(
    "static_ip", [{"region": None}, {"region": "us-central1"}], indirect=True
)
def test_get_static_ip(static_ip: Address):
    region = static_ip.region.split("/")[-1] if static_ip.region else None
    actual_address = get_static_ip_address(
        project_id=PROJECT, address_name=static_ip.name, region=region
    )
    assert static_ip.region in actual_address.region
    assert static_ip.name == actual_address.name


def test_get_instance_external_ip_address(instance_with_ips):
    # Internal IP check
    internal_ips = get_instance_ip_address(instance_with_ips, ip_type=IPType.INTERNAL)
    expected_internal_ips = {
        interface.network_i_p for interface in instance_with_ips.network_interfaces
    }
    assert set(internal_ips) == expected_internal_ips, "Internal IPs do not match"

    # External IP check
    external_ips = get_instance_ip_address(instance_with_ips, ip_type=IPType.EXTERNAL)
    expected_external_ips = {
        config.nat_i_p
        for interface in instance_with_ips.network_interfaces
        for config in interface.access_configs
        if config.type_ == "ONE_TO_ONE_NAT"
    }
    assert set(external_ips) == expected_external_ips, "External IPs do not match"

    # IPv6 IP check
    ipv6_ips = get_instance_ip_address(instance_with_ips, ip_type=IPType.IP_V6)
    expected_ipv6_ips = {
        ipv6_config.external_ipv6
        for interface in instance_with_ips.network_interfaces
        for ipv6_config in getattr(interface, "ipv6_access_configs", [])
        if ipv6_config.type_ == "DIRECT_IPV6"
    }
    assert set(ipv6_ips) == expected_ipv6_ips, "IPv6 IPs do not match"
