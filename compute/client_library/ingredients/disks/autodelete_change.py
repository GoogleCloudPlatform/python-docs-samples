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

from google.cloud import compute_v1


# <INGREDIENT set_disk_autodelete>
def set_disk_autodelete(project_id: str, zone: str, instance_name: str, disk_name: str, autodelete: bool) -> None:
    """
    Set the autodelete flag of a disk to given value.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which is the disk you want to modify.
        instance_name: name of the instance the disk is attached to.
        disk_name: the name of the disk which flag you want to modify.
        autodelete: the new value of the autodelete flag.
    """
    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(project=project_id, zone=zone, instance=instance_name)

    for disk in instance.disks:
        if disk.device_name == disk_name:
            break
    else:
        raise RuntimeError(f"Instance {instance_name} doesn't have a disk named {disk_name} attached.")

    disk.auto_delete = autodelete

    operation = instance_client.update(project=project_id, zone=zone, instance=instance_name, instance_resource=instance)

    wait_for_extended_operation(operation, "disk update")
# </INGREDIENT>
