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

from google.cloud.compute_v1.services.addresses.client import AddressesClient
from google.cloud.compute_v1.services.global_addresses import GlobalAddressesClient


# <INGREDIENT release_external_ip_address>
def release_external_ip_address(
    project_id: str,
    address_name: str,
    region: Optional[str] = None,
) -> None:
    """
    Releases a static external IP address that is currently reserved.
    This action requires that the address is not being used by any forwarding rule.

    Args:
        project_id (str): project ID.
        address_name (str): name of the address to release.
        region (Optional[str]): The region to reserve the IP address in, if regional. Must be None if global.


    """
    if not region:  # global IP address
        client = GlobalAddressesClient()
        operation = client.delete(project=project_id, address=address_name)
    else:  # regional IP address
        client = AddressesClient()
        operation = client.delete(
            project=project_id, region=region, address=address_name
        )

    operation.result()
    print(f"External IP address '{address_name}' released successfully.")


# </INGREDIENT>
