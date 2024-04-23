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

from typing import List, Optional, Union
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
from ..instances.ip_address.reserve_new_external_ip_address import (
    reserve_new_external_ip_address,
)

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


def delete_ip_address(
    client: Union[AddressesClient, GlobalAddressesClient],
    project_id: str,
    address_name: str,
    region: Optional[str] = None,
):
    """
    Deletes ip address with given parameters.
    Args:
        client (Union[AddressesClient, GlobalAddressesClient]): global or regional address client
        project_id (str): project id
        address_name (str): ip address name to delete
        region (Optional[str]): region of ip address. Marker to choose between clients (GlobalAddressesClient when None)
    """
    if region:
        operation = client.delete(
            project=project_id, region=region, address=address_name
        )
    else:
        operation = client.delete(project=project_id, address=address_name)
    operation.result()


def list_ip_addresses(
    client: Union[AddressesClient, GlobalAddressesClient],
    project_id: str,
    region: Optional[str] = None,
) -> List[str]:
    """
    Retrieves ip address names of project (global) or region.
    Args:
        client (Union[AddressesClient, GlobalAddressesClient]): global or regional address client
        project_id (str): project id
        region (Optional[str]): region of ip address. Marker to choose between clients (GlobalAddressesClient when None)

    Returns:
        list of ip address names as strings
    """
    if region:
        return [
            address.name for address in client.list(project=project_id, region=region)
        ]
    return [address.name for address in client.list(project=project_id)]


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


def test_reserve_new_external_ip_address_global():
    global_client = GlobalAddressesClient()
    unique_string = uuid.uuid4()
    ip_4_global = f"ip4-global-{unique_string}"
    ip_6_global = f"ip6-global-{unique_string}"

    expected_ips = {ip_4_global, ip_6_global}
    try:
        # ip4 global
        reserve_new_external_ip_address(PROJECT, ip_4_global)
        # ip6 global
        reserve_new_external_ip_address(PROJECT, ip_6_global, is_v6=True)

        ips = list_ip_addresses(global_client, PROJECT)
        assert set(ips).issuperset(expected_ips)
    finally:
        # cleanup
        for address in expected_ips:
            delete_ip_address(global_client, PROJECT, address)


def test_reserve_new_external_ip_address_regional():
    regional_client = AddressesClient()
    unique_string = uuid.uuid4()
    region = "us-central1"

    ip_4_regional = f"ip4-regional-{unique_string}"
    ip_4_regional_premium = f"ip4-regional-premium-{unique_string}"
    ip_6_regional = f"ip6-regional-{unique_string}"
    ip_6_regional_premium = f"ip6-regional-premium-{unique_string}"

    expected_ips = {
        ip_4_regional,
        ip_4_regional_premium,
        ip_6_regional,
        ip_6_regional_premium,
    }
    try:
        # ip4 regional standard
        reserve_new_external_ip_address(PROJECT, ip_4_regional, region=region)
        # ip4 regional premium
        reserve_new_external_ip_address(
            PROJECT, ip_4_regional_premium, region=region, is_premium=True
        )
        # ip6 regional standard
        reserve_new_external_ip_address(
            PROJECT, ip_6_regional, region=region, is_v6=True
        )
        # ip6 regional premium
        reserve_new_external_ip_address(
            PROJECT, ip_6_regional_premium, region=region, is_premium=True, is_v6=True
        )

        ips = list_ip_addresses(regional_client, PROJECT, region=region)
        assert set(ips).issuperset(expected_ips)
    finally:
        # cleanup
        for address in expected_ips:
            delete_ip_address(regional_client, PROJECT, address, region=region)
