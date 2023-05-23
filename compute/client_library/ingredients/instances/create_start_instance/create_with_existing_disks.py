#  Copyright 2022 Google LLC
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
from __future__ import annotations


from google.cloud import compute_v1


# <INGREDIENT create_with_existing_disks>
def create_with_existing_disks(project_id: str, zone: str, instance_name: str, disk_names: list[str]) -> compute_v1.Instance:
    """
    Create a new VM instance using selected disks. The first disk in disk_names will
    be used as boot disk.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        disk_names: list of disk names to be attached to the new virtual machine.
            First disk in this list will be used as the boot device.

    Returns:
        Instance object.
    """
    assert len(disk_names) >= 1
    disks = [get_disk(project_id, zone, disk_name) for disk_name in disk_names]
    attached_disks = []
    for disk in disks:
        adisk = compute_v1.AttachedDisk()
        adisk.source = disk.self_link
        attached_disks.append(adisk)
    attached_disks[0].boot = True
    instance = create_instance(project_id, zone, instance_name, attached_disks)
    return instance
# </INGREDIENT>
