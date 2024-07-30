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
from typing import List, Optional

from google.cloud.compute_v1.types import Address
from google.cloud.compute_v1.services.addresses.client import AddressesClient
from google.cloud.compute_v1.services.global_addresses import GlobalAddressesClient


# <INGREDIENT list_static_ip_addresses>
def list_static_ip_addresses(
    project_id: str, region: Optional[str] = None
) -> List[Address]:
    """
    Lists all static external IP addresses, either regional or global.

    Args:
    project_id (str): project ID.
    region (Optional[str]): The region of the IP addresses if regional. None if global.

    Returns:
    List[Address]: A list of Address objects containing details about the requested IPs.
    """
    if region:
        # Use regional client if a region is specified
        client = AddressesClient()
        addresses_iterator = client.list(project=project_id, region=region)
    else:
        # Use global client if no region is specified
        client = GlobalAddressesClient()
        addresses_iterator = client.list(project=project_id)

    return list(addresses_iterator)  # Convert the iterator to a list to return


# </INGREDIENT>
