# Copyright 2023 Google LLC
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

# [START vmwareengine_create_policy]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def create_network_policy(
    project_id: str,
    region: str,
    ip_range: str,
    internet_access: bool,
    external_ip: bool,
) -> operation.Operation:
    """
    Creates a new network policy in a given network.

    Args:
        project_id: name of the project you want to use.
        region: name of the region you want to use. I.e. "us-central1"
        ip_range: the CIDR range to use for internet access and external IP access gateways,
            in CIDR notation. An RFC 1918 CIDR block with a "/26" suffix is required.
        internet_access: should internet access be allowed.
        external_ip: should external IP addresses be assigned.

    Returns:
        An operation object representing the started operation. You can call its .result() method to wait for
        it to finish.

    Raises:
        ValueError if the provided ip_range doesn't end with /26.
    """
    if not ip_range.endswith("/26"):
        raise ValueError(
            "The ip_range needs to be an RFC 1918 CIDR block with a '/26' suffix"
        )

    network_policy = vmwareengine_v1.NetworkPolicy()
    network_policy.vmware_engine_network = f"projects/{project_id}/locations/{region}/vmwareEngineNetworks/{region}-default"
    network_policy.edge_services_cidr = ip_range
    network_policy.internet_access.enabled = internet_access
    network_policy.external_ip.enabled = external_ip

    request = vmwareengine_v1.CreateNetworkPolicyRequest()
    request.network_policy = network_policy
    request.parent = f"projects/{project_id}/locations/{region}"
    request.network_policy_id = f"{region}-default"

    client = vmwareengine_v1.VmwareEngineClient()
    return client.create_network_policy(request)


# [END vmwareengine_create_policy]
