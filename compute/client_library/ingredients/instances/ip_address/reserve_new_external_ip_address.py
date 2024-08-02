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
# flake8: noqa
from typing import Optional

from google.cloud.compute_v1.types import Address
from google.cloud.compute_v1.services.addresses.client import AddressesClient
from google.cloud.compute_v1.services.global_addresses import GlobalAddressesClient


# <INGREDIENT reserve_new_external_ip_address>
def reserve_new_external_ip_address(
    project_id: str,
    address_name: str,
    is_v6: bool = False,
    is_premium: bool = False,
    region: Optional[str] = None,
):
    """
    Reserves a new external IP address in the specified project and region.

    Args:
    project_id (str): Your Google Cloud project ID.
    address_name (str): The name for the new IP address.
    is_v6 (bool): 'IPV4' or 'IPV6' depending on the IP version. IPV6 if True.
    is_premium (bool): 'STANDARD' or 'PREMIUM' network tier. Standard option available only in regional ip.
    region (Optional[str]): The region to reserve the IP address in, if regional. Must be None if global.

    Returns:
    None
    """

    ip_version = "IPV6" if is_v6 else "IPV4"
    network_tier = "STANDARD" if not is_premium and region else "PREMIUM"

    address = Address(
        name=address_name,
        address_type="EXTERNAL",
        network_tier=network_tier,
    )
    if not region:  # global IP address
        client = GlobalAddressesClient()
        address.ip_version = ip_version
        operation = client.insert(project=project_id, address_resource=address)
    else:  # regional IP address
        address.region = region
        client = AddressesClient()
        operation = client.insert(
            project=project_id, region=region, address_resource=address
        )

    operation.result()

    print(f"External IP address '{address_name}' reserved successfully.")


# </INGREDIENT>
