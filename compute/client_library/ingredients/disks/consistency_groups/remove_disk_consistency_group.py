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


# <INGREDIENT remove_disk_from_consistency_group>
def remove_disk_consistency_group(
    project_id: str,
    disk_name: str,
    disk_location: str,
    consistency_group_name: str,
    consistency_group_region: str,
) -> None:
    """Removes a disk from a specified consistency group.
    Args:
        project_id (str): The ID of the Google Cloud project.
        disk_name (str): The name of the disk to be deleted.
        disk_location (str): The region or zone of the disk
        consistency_group_name (str): The name of the consistency group.
        consistency_group_region (str): The region of the consistency group.
    Returns:
        None
    """
    consistency_group_link = (
        f"regions/{consistency_group_region}/resourcePolicies/{consistency_group_name}"
    )
    # Checking if the disk is zonal or regional
    # If the final character of the disk_location is a digit, it is a regional disk
    if disk_location[-1].isdigit():
        policy = compute_v1.RegionDisksRemoveResourcePoliciesRequest(
            resource_policies=[consistency_group_link]
        )
        disk_client = compute_v1.RegionDisksClient()
        disk_client.remove_resource_policies(
            project=project_id,
            region=disk_location,
            disk=disk_name,
            region_disks_remove_resource_policies_request_resource=policy,
        )
    # For zonal disks we use DisksClient
    else:
        policy = compute_v1.DisksRemoveResourcePoliciesRequest(
            resource_policies=[consistency_group_link]
        )
        disk_client = compute_v1.DisksClient()
        disk_client.remove_resource_policies(
            project=project_id,
            zone=disk_location,
            disk=disk_name,
            disks_remove_resource_policies_request_resource=policy,
        )

    print(f"Disk {disk_name} removed from consistency group {consistency_group_name}")


# </INGREDIENT>
