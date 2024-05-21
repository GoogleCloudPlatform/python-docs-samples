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
import uuid

from google.cloud.compute_v1 import AddressesClient
from google.cloud.compute_v1.types import Address

# <INGREDIENT promote_ephemeral_ip>


def promote_ephemeral_ip(project_id: str, ephemeral_ip: str, region: str):
    """
    Promote ephemeral IP found on the instance to a static IP.

    Args:
        project_id (str): Project ID.
        ephemeral_ip (str): Ephemeral IP address to promote.
        region (str): Region where the VM and IP is located.
    """
    addresses_client = AddressesClient()

    # Create a new static IP address using existing ephemeral IP
    address_resource = Address(
        name=f"ip-reserved-{uuid.uuid4()}",  # new name for promoted IP address
        region=region,
        address_type="EXTERNAL",
        address=ephemeral_ip,
    )
    operation = addresses_client.insert(
        project=project_id, region=region, address_resource=address_resource
    )
    operation.result()

    print(f"Ephemeral IP {ephemeral_ip} has been promoted to a static IP.")


# </INGREDIENT>
