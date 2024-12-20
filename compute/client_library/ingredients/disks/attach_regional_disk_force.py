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


# <INGREDIENT attach_disk_force>


def attach_disk_force(
    project_id: str, vm_name: str, vm_zone: str, disk_name: str, disk_region: str
) -> None:
    """
    Force-attaches a regional disk to a compute instance, even if it is
    still attached to another instance. Useful when the original instance
    cannot be reached or disconnected.
    Args:
        project_id (str): The ID of the Google Cloud project.
        vm_name (str): The name of the compute instance you want to attach a disk to.
        vm_zone (str): The zone where the compute instance is located.
        disk_name (str): The name of the disk to be attached.
        disk_region (str): The region where the disk is located.
    Returns:
        None
    """
    client = compute_v1.InstancesClient()
    disk = compute_v1.AttachedDisk(
        source=f"projects/{project_id}/regions/{disk_region}/disks/{disk_name}"
    )

    request = compute_v1.AttachDiskInstanceRequest(
        attached_disk_resource=disk,
        force_attach=True,
        instance=vm_name,
        project=project_id,
        zone=vm_zone,
    )
    operation = client.attach_disk(request=request)
    wait_for_extended_operation(operation, "force disk attachment")


# </INGREDIENT>
