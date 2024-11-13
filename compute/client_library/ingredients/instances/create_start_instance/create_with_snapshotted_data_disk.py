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


# <INGREDIENT create_with_snapshotted_data_disk>
def create_with_snapshotted_data_disk(
    project_id: str, zone: str, instance_name: str, snapshot_link: str
):
    """
    Create a new VM instance with Debian 10 operating system and data disk created from snapshot.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        snapshot_link: link to the snapshot you want to use as the source of your
            data disk in the form of: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        Instance object.
    """
    newest_debian = get_image_from_family(project="debian-cloud", family="debian-12")
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [
        disk_from_image(disk_type, 10, True, newest_debian.self_link),
        disk_from_snapshot(disk_type, 11, False, snapshot_link),
    ]
    instance = create_instance(project_id, zone, instance_name, disks)
    return instance


# </INGREDIENT>
