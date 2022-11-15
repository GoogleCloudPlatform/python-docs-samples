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

from google.cloud import compute_v1


# <INGREDIENT create_firewall_rule_for_windows_activation_host>
def create_firewall_rule_for_windows_activation_host(
    project_id: str, firewall_rule_name: str, network: str = "global/networks/default"
) -> compute_v1.Firewall:
    """
    Creates an egress firewall rule with the highest priority for host
    kms.windows.googlecloud.com (35.190.247.13) for Windows activation.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        firewall_rule_name: name of the rule that is created.
        network: name of the network the rule will be applied to. Available name formats:
            * https://www.googleapis.com/compute/v1/projects/{project_id}/global/networks/{network}
            * projects/{project_id}/global/networks/{network}
            * global/networks/{network}

    Returns:
        A Firewall object.
    """
    firewall_rule = compute_v1.Firewall()
    firewall_rule.name = firewall_rule_name
    firewall_rule.network = network

    allowed = compute_v1.Allowed()
    allowed.ports = ['1688']
    allowed.I_p_protocol = 'tcp'

    firewall_rule.allowed = [allowed]
    firewall_rule.destination_ranges = ["35.190.247.13/32"]
    firewall_rule.direction = compute_v1.Firewall.Direction.EGRESS.name
    firewall_rule.priority = 0

    firewall_client = compute_v1.FirewallsClient()
    operation = firewall_client.insert(project=project_id, firewall_resource=firewall_rule)

    wait_for_extended_operation(operation, "windows KSM firewall rule creation")

    return firewall_client.get(project=project_id, firewall=firewall_rule_name)
# </INGREDIENT>

