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


# <INGREDIENT delete_managed_instance_group>
def delete_managed_instance_group(
    project_id: str,
    zone: str,
    group_name: str,
) -> None:
    """
    Send a managed group instance deletion request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        group_name: the name for this instance group.
    Returns:
        Instance group manager object.
    """
    instance_client = compute_v1.InstanceGroupManagersClient()

    # Prepare the request to delete an instance.
    request = compute_v1.DeleteInstanceGroupManagerRequest()
    request.zone = zone
    request.project = project_id
    request.instance_group_manager = group_name

    # Wait for the create operation to complete.
    print(f"Deleting the {group_name} group in {zone}...")

    operation = instance_client.delete(request=request)

    wait_for_extended_operation(operation, "instance deletion")

    print(f"Group {group_name} deleted.")
    return None


# </INGREDIENT>
