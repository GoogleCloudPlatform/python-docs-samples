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
from typing import List

from google.cloud import compute_v1
from enum import Enum


# <INGREDIENT get_instance_ip_address>
class IPType(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    IP_V6 = "ipv6"


def get_instance_ip_address(
    instance: compute_v1.Instance, ip_type: IPType
) -> List[str]:
    """
    Retrieves the specified type of IP address (ipv6, internal or external) of a specified Compute Engine instance.

    Args:
        instance (compute_v1.Instance): instance to get
        ip_type (IPType): The type of IP address to retrieve (ipv6, internal or external).

    Returns:
        List[str]: Requested type IP addresses of the instance.
    """
    ips = []
    if not instance.network_interfaces:
        return ips
    for interface in instance.network_interfaces:
        if ip_type == IPType.EXTERNAL:
            for config in interface.access_configs:
                if config.type_ == "ONE_TO_ONE_NAT":
                    ips.append(config.nat_i_p)
        elif ip_type == IPType.IP_V6:
            for ipv6_config in getattr(interface, "ipv6_access_configs", []):
                if ipv6_config.type_ == "DIRECT_IPV6":
                    ips.append(ipv6_config.external_ipv6)

        elif ip_type == IPType.INTERNAL:
            # Internal IP is directly available in the network interface
            ips.append(interface.network_i_p)
    return ips


# </INGREDIENT>
