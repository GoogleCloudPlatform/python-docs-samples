#  Copyright 2022 Google LLC
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

# <REGION compute_create_route_windows_activation>
# <IMPORTS/>

# <INGREDIENT wait_for_extended_operation />

# <INGREDIENT create_route />

def create_route_to_windows_activation_host(project_id: str, network: str, route_name: str) -> compute_v1.Route:
    """
    If you have Windows instances without external IP addresses,
    you must also enable Private Google Access so that instances
    with only internal IP addresses can send traffic to the external
    IP address for kms.windows.googlecloud.com.
    More infromation: https://cloud.google.com/vpc/docs/configure-private-google-access#enabling

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        network: name of the network the route will be created in. Available name formats:
            * https://www.googleapis.com/compute/v1/projects/{project_id}/global/networks/{network}
            * projects/{project_id}/global/networks/{network}
            * global/networks/{network}
        route_name: name of the new route.

    Returns:
        A new compute_v1.Route object.
    """
    return create_route(project_id=project_id, network=network, route_name=route_name,
                        destination_range='35.190.247.13/32',
                        next_hop_gateway=f"projects/{project_id}/global/gateways/default-internet-gateway")
# </REGION compute_create_route_windows_activation>
