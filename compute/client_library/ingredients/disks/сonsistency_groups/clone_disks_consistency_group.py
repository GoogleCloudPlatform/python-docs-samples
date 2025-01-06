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


# <INGREDIENT consistency_group_clone_disks>
def clone_disks_to_consistency_group(project_id, group_region, group_name):
    """
    Clones disks to a consistency group in the specified region.
    Args:
        project_id (str): The ID of the Google Cloud project.
        group_region (str): The region where the consistency group is located.
        group_name (str): The name of the consistency group.
    Returns:
        bool: True if the disks were successfully cloned to the consistency group.
    """
    consistency_group_policy = (
        f"projects/{project_id}/regions/{group_region}/resourcePolicies/{group_name}"
    )

    resource = compute_v1.BulkInsertDiskResource(
        source_consistency_group_policy=consistency_group_policy
    )
    client = compute_v1.RegionDisksClient()
    request = compute_v1.BulkInsertRegionDiskRequest(
        project=project_id,
        region=group_region,
        bulk_insert_disk_resource_resource=resource,
    )
    operation = client.bulk_insert(request=request)
    wait_for_extended_operation(operation, verbose_name="bulk insert disk")
    return True


# </INGREDIENT>
