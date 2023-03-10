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


# <INGREDIENT patch_firewall_priority>
def patch_firewall_priority(project_id: str, firewall_rule_name: str, priority: int) -> None:
    """
    Modifies the priority of a given firewall rule.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        firewall_rule_name: name of the rule you want to modify.
        priority: the new priority to be set for the rule.
    """
    firewall_rule = compute_v1.Firewall()
    firewall_rule.priority = priority

    # The patch operation doesn't require the full definition of a Firewall object. It will only update
    # the values that were set in it, in this case it will only change the priority.
    firewall_client = compute_v1.FirewallsClient()
    operation = firewall_client.patch(
        project=project_id, firewall=firewall_rule_name, firewall_resource=firewall_rule
    )

    wait_for_extended_operation(operation, "firewall rule patching")
# </INGREDIENT>
