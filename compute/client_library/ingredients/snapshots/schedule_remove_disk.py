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


# <INGREDIENT remove_disk_schedule_snapshots>
def snapshot_schedule_detach_disk(
    project_id: str, zone: str, region: str, disk_name: str, schedule_name: str
) -> None:
    """
    Detaches a snapshot schedule from a specified disk in a given project and zone.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the disk is located.
        region (str): The location of the snapshot schedule
        disk_name (str): The name of the disk with the associated snapshot schedule
        schedule_name (str): The name of the snapshot schedule that you are removing from this disk
    Returns:
        None
    """
    disks_remove_request = compute_v1.DisksRemoveResourcePoliciesRequest(
        resource_policies=[f"regions/{region}/resourcePolicies/{schedule_name}"]
    )

    client = compute_v1.DisksClient()
    operation = client.remove_resource_policies(
        project=project_id,
        zone=zone,
        disk=disk_name,
        disks_remove_resource_policies_request_resource=disks_remove_request,
    )
    wait_for_extended_operation(operation, "Detaching snapshot schedule from disk")


# </INGREDIENT>
