#  Copyright 2023 Google LLC
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


# <INGREDIENT attach_disk>
def attach_disk(
        project_id: str,
        zone: str,
        instance_name: str,
        disk_link: str,
        mode: str
) -> None:
    """
    Attaches a non-boot persistent disk to a specified compute instance. The disk might be zonal or regional.

    You need following permissions to execute this action:
    https://cloud.google.com/compute/docs/disks/regional-persistent-disk#expandable-1

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone:name of the zone in which the instance you want to use resides.
        instance_name: name of the compute instance you want to attach a disk to.
        disk_link: full or partial URL to a persistent disk that you want to attach. This can be either
            regional or zonal disk.
            Expected formats:
                * https://www.googleapis.com/compute/v1/projects/[project]/zones/[zone]/disks/[disk_name]
                * /projects/[project]/zones/[zone]/disks/[disk_name]
                * /projects/[project]/regions/[region]/disks/[disk_name]
        mode: Specifies in what mode the disk will be attached to the instance. Available options are `READ_ONLY`
            and `READ_WRITE`. Disk in `READ_ONLY` mode can be attached to multiple instances at once.
    """
    instances_client = compute_v1.InstancesClient()

    request = compute_v1.AttachDiskInstanceRequest()
    request.project = project_id
    request.zone = zone
    request.instance = instance_name
    request.attached_disk_resource = compute_v1.AttachedDisk()
    request.attached_disk_resource.source = disk_link
    request.attached_disk_resource.mode = mode

    operation = instances_client.attach_disk(request)

    wait_for_extended_operation(operation, "disk attachement")
# </INGREDIENT>
