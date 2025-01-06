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


# <INGREDIENT attach_regional_disk>
def attach_regional_disk(
    project_id: str, zone: str, instance_name: str, disk_region: str, disk_name: str
) -> None:
    """
    Attaches a regional disk to a specified compute instance.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the instance is located.
        instance_name (str): The name of the instance to which the disk will be attached.
        disk_region (str): The region where the disk is located.
        disk_name (str): The name of the disk to be attached.
    Returns:
        None
    """
    instances_client = compute_v1.InstancesClient()

    disk_resource = compute_v1.AttachedDisk(
        source=f"/projects/{project_id}/regions/{disk_region}/disks/{disk_name}"
    )

    operation = instances_client.attach_disk(
        project=project_id,
        zone=zone,
        instance=instance_name,
        attached_disk_resource=disk_resource,
    )
    wait_for_extended_operation(operation, "regional disk attachment")


# </INGREDIENT>
