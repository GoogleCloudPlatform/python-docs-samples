# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Examples of working with clients for Security Command Center."""
# [START securitycenter_set_client_endpoint_v2]
from typing import Dict


def create_client_with_endpoint(api_endpoint) -> Dict:
    """
    Creates Security Command Center clients for a regional endpoint and the default endpoint.
    Args:
        api_endpoint: the regional endpoint's hostname, like 'securitycenter.REGION.rep.googleapis.com'
    Returns:
        Dict: Returns clients with the default and regional endpoints; each key is a hostname
    """
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()
    regional_client = securitycenter.SecurityCenterClient(
        client_options={"api_endpoint": api_endpoint}
    )
    print("Client initiated with endpoint: {}".format(client.api_endpoint))
    print("Regional client initiated with endpoint: {}".format(regional_client.api_endpoint))
    return {
        client.api_endpoint: client,
        regional_client.api_endpoint: regional_client,
    }
# [END securitycenter_set_client_endpoint_v2]
