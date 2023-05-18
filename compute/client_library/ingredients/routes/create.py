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

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa
from __future__ import annotations


from google.cloud import compute_v1


# <INGREDIENT create_route>
def create_route(project_id: str, network: str, route_name: str, destination_range: str, *,
                 next_hop_gateway: str | None = None,
                 next_hop_ip: str | None = None, next_hop_instance: str | None = None,
                 next_hop_vpn_tunnel: str | None = None, next_hop_ilb: str | None = None) -> compute_v1.Route:
    """
    Create a new route in selected network by providing a destination and next hop name.

    Note: The set of {next_hop_gateway, next_hop_ip, next_hop_instance, next_hop_vpn_tunnel,
        next_hop_ilb} is exclusive, you and only specify one of those parameters.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        network: name of the network the route will be created in. Available name formats:
            * https://www.googleapis.com/compute/v1/projects/{project_id}/global/networks/{network}
            * projects/{project_id}/global/networks/{network}
            * global/networks/{network}
        route_name: name of the new route.
        destination_range: range of destination IPs this route should be applied to. E.g. 10.0.0.0/16.
        next_hop_gateway: name of the gateway the traffic should be directed to.
        next_hop_ip: IP address the traffic should be directed to.
        next_hop_instance: name of the instance the traffic should be directed to. Name format:
            "projects/{project}/zones/{zone}/instances/{instance_name}"
        next_hop_vpn_tunnel: name of the VPN tunnel the traffic should be directed to. Name format:
            "projects/{project}/regions/{region}/vpnTunnels/{vpn_tunnel_name}"
        next_hop_ilb: name of a forwarding rule of the Internal Load Balancer the traffic
            should be directed to. Name format:
            "projects/{project}/regions/{region}/forwardingRules/{forwarding_rule_region}"

    Returns:
        A new compute_v1.Route object.
    """
    excl_args = {next_hop_instance, next_hop_ilb, next_hop_vpn_tunnel, next_hop_gateway, next_hop_ip}
    args_set = sum(1 if arg is not None else 0 for arg in excl_args)

    if args_set != 1:
        raise RuntimeError("You must specify exactly one next_hop_* parameter.")

    route = compute_v1.Route()
    route.name = route_name
    route.network = network
    route.dest_range = destination_range

    if next_hop_gateway:
        route.next_hop_gateway = next_hop_gateway
    elif next_hop_ip:
        route.next_hop_ip = next_hop_ip
    elif next_hop_instance:
        route.next_hop_instance = next_hop_instance
    elif next_hop_vpn_tunnel:
        route.next_hop_vpn_tunnel = next_hop_vpn_tunnel
    elif next_hop_ilb:
        route.next_hop_ilb = next_hop_ilb

    route_client = compute_v1.RoutesClient()
    operation = route_client.insert(project=project_id, route_resource=route)

    wait_for_extended_operation(operation, "route creation")

    return route_client.get(project=project_id, route=route_name)
# </INGREDIENT>
