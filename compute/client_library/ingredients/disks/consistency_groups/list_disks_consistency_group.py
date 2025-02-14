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


# <INGREDIENT list_disks_in_consistency_group>
def list_disks_consistency_group(
    project_id: str,
    disk_location: str,
    consistency_group_name: str,
    consistency_group_region: str,
) -> list:
    """
    Lists disks that are part of a specified consistency group.
    Args:
        project_id (str): The ID of the Google Cloud project.
        disk_location (str): The region or zone of the disk
        disk_region_flag (bool): Flag indicating if the disk is regional.
        consistency_group_name (str): The name of the consistency group.
        consistency_group_region (str): The region of the consistency group.
    Returns:
        list: A list of disks that are part of the specified consistency group.
    """
    consistency_group_link = (
        f"https://www.googleapis.com/compute/v1/projects/{project_id}/regions/"
        f"{consistency_group_region}/resourcePolicies/{consistency_group_name}"
    )
    # If the final character of the disk_location is a digit, it is a regional disk
    if disk_location[-1].isdigit():
        region_client = compute_v1.RegionDisksClient()
        disks = region_client.list(project=project_id, region=disk_location)
    # For zonal disks we use DisksClient
    else:
        client = compute_v1.DisksClient()
        disks = client.list(project=project_id, zone=disk_location)
    return [disk for disk in disks if consistency_group_link in disk.resource_policies]


# </INGREDIENT>
