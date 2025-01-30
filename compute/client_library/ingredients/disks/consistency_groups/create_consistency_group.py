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

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT consistency_group_create>
def create_consistency_group(
    project_id: str, region: str, group_name: str, group_description: str
) -> compute_v1.ResourcePolicy:
    """
    Creates a consistency group in Google Cloud Compute Engine.
    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the consistency group will be created.
        group_name (str): The name of the consistency group.
        group_description (str): The description of the consistency group.
    Returns:
        compute_v1.ResourcePolicy: The consistency group object
    """

    # Initialize the ResourcePoliciesClient
    client = compute_v1.ResourcePoliciesClient()

    # Create the ResourcePolicy object with the provided name, description, and policy
    resource_policy_resource = compute_v1.ResourcePolicy(
        name=group_name,
        description=group_description,
        disk_consistency_group_policy=compute_v1.ResourcePolicyDiskConsistencyGroupPolicy(),
    )

    operation = client.insert(
        project=project_id,
        region=region,
        resource_policy_resource=resource_policy_resource,
    )
    wait_for_extended_operation(operation, "Consistency group creation")

    return client.get(project=project_id, region=region, resource_policy=group_name)


# </INGREDIENT>
