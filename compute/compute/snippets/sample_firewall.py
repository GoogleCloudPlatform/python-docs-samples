# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Iterable

# [START compute_firewall_list]
# [START compute_firewall_create]
# [START compute_firewall_patch]
# [START compute_firewall_delete]
import google.cloud.compute_v1 as compute_v1
# [END compute_firewall_delete]
# [END compute_firewall_patch]
# [END compute_firewall_create]
# [END compute_firewall_list]


# [START compute_firewall_list]
def list_firewall_rules(project_id: str) -> Iterable:
    """
    Return a list of all the firewall rules in specified project. Also prints the
    list of firewall names and their descriptions.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.

    Returns:
    A flat list of all firewall rules defined for given project.
    """
    firewall_client = compute_v1.FirewallsClient()
    firewalls_list = firewall_client.list(project=project_id)

    for firewall in firewalls_list:
        print(f" - {firewall.name}: {firewall.description}")

    return firewalls_list
# [END compute_firewall_list]


def print_firewall_rule(project_id: str, firewall_rule_name: str):
    firewall_client = compute_v1.FirewallsClient()
    print(firewall_client.get(project=project_id, firewall=firewall_rule_name))


# [START compute_firewall_create]
def create_firewall_rule(
    project_id: str, firewall_rule_name: str, network: str = "global/networks/default"
):
    """
    Creates a simple firewall rule allowing for incoming HTTP and HTTPS access from the entire Internet.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        firewall_rule_name: name of the rule that is created.
        network: name of the network the rule will be applied to. Available name formats:
            * https://www.googleapis.com/compute/v1/projects/{project_id}/global/networks/{network}
            * projects/{project_id}/global/networks/{network}
            * global/networks/{network}
    """
    firewall_rule = compute_v1.Firewall()
    firewall_rule.name = firewall_rule_name
    firewall_rule.direction = compute_v1.Firewall.Direction.INGRESS

    tcp_80_443_allowed = compute_v1.Allowed()
    tcp_80_443_allowed.I_p_protocol = "tcp"
    tcp_80_443_allowed.ports = ["80", "443"]

    firewall_rule.allowed = [tcp_80_443_allowed]
    firewall_rule.source_ranges = ["0.0.0.0/0"]
    firewall_rule.network = network
    firewall_rule.description = "Allowing TCP traffic on port 80 and 443 from Internet."

    # Note that the default value of priority for the firewall API is 1000.
    # If you check the value of `firewall_rule.priority` at this point it
    # will be equal to 0, however it is not treated as "set" by the library and thus
    # the default will be applied to the new rule. If you want to create a rule that
    # has priority == 0, you need to explicitly set it so:

    # firewall_rule.priority = 0

    firewall_client = compute_v1.FirewallsClient()
    op = firewall_client.insert(project=project_id, firewall_resource=firewall_rule)

    op_client = compute_v1.GlobalOperationsClient()
    op_client.wait(project=project_id, operation=op.name)

    return
# [END compute_firewall_create]


# [START compute_firewall_patch]
def patch_firewall_priority(project_id: str, firewall_rule_name: str, priority: int):
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

    operation_client = compute_v1.GlobalOperationsClient()
    operation_client.wait(project=project_id, operation=operation.name)
    return
# [END compute_firewall_patch]


# [START compute_firewall_delete]
def delete_firewall_rule(project_id: str, firewall_rule_name: str):
    """
    Deleted a firewall rule from the project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        firewall_rule_name: name of the firewall rule you want to delete.
    """
    firewall_client = compute_v1.FirewallsClient()
    operation = firewall_client.delete(project=project_id, firewall=firewall_rule_name)

    operation_client = compute_v1.GlobalOperationsClient()
    operation_client.wait(project=project_id, operation=operation.name)
    return
# [END compute_firewall_delete]


if __name__ == "__main__":
    import google.auth
    import google.auth.exceptions

    try:
        default_project_id = google.auth.default()[1]
        print(f"Using project {default_project_id}.")
    except google.auth.exceptions.DefaultCredentialsError:
        print(
            "Please use `gcloud auth application-default login` "
            "or set GOOGLE_APPLICATION_CREDENTIALS to use this script."
        )
    else:
        import uuid

        rule_name = "firewall-sample-" + uuid.uuid4().hex[:10]
        print(f"Creating firewall rule {rule_name}...")
        # The rule will be created with default priority of 1000.
        create_firewall_rule(default_project_id, rule_name)
        try:
            print("Rule created:")
            print_firewall_rule(default_project_id, rule_name)
            print("Updating rule priority to 10...")
            patch_firewall_priority(default_project_id, rule_name, 10)
            print("Rule updated: ")
            print_firewall_rule(default_project_id, rule_name)
            print(f"Deleting rule {rule_name}...")
        finally:
            delete_firewall_rule(default_project_id, rule_name)
        print("Done.")
