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
from google.cloud import securitycenter_v2


def create_client_with_endpoint(api_endpoint) -> securitycenter_v2.SecurityCenterClient:
    """
    Creates a Security Command Center client for a regional endpoint.
    Args:
        api_endpoint: the regional endpoint's hostname, like 'securitycenter.REGION.rep.googleapis.com'
    Returns:
        securitycenter_v2.SecurityCenterClient: returns a client for the regional endpoint
    """
    regional_client = securitycenter_v2.SecurityCenterClient(
        client_options={"api_endpoint": api_endpoint}
    )
    print(
        "Regional client initiated with endpoint: {}".format(
            regional_client.api_endpoint
        )
    )
    return regional_client


# [END securitycenter_set_client_endpoint_v2]
