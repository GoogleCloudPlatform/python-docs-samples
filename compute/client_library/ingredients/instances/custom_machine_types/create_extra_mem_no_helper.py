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
from typing import List

from google.cloud import compute_v1


# <INGREDIENT create_custom_instances_extra_mem>
def create_custom_instances_extra_mem(
    project_id: str, zone: str, instance_name: str, core_count: int, memory: int
) -> List[compute_v1.Instance]:
    """
    Create 3 new VM instances with extra memory without using a CustomMachineType helper class.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        core_count: number of CPU cores you want to use.
        memory: the amount of memory for the VM instance, in megabytes.

    Returns:
        List of Instance objects.
    """
    newest_debian = get_image_from_family(
        project="debian-cloud", family="debian-10"
    )
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link)]
    # The core_count and memory values are not validated anywhere and can be rejected by the API.
    instances = [
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n1_extra_mem",
            disks,
            f"zones/{zone}/machineTypes/custom-{core_count}-{memory}-ext",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n2_extra_mem",
            disks,
            f"zones/{zone}/machineTypes/n2-custom-{core_count}-{memory}-ext",
        ),
        create_instance(
            project_id,
            zone,
            f"{instance_name}_n2d_extra_mem",
            disks,
            f"zones/{zone}/machineTypes/n2d-custom-{core_count}-{memory}-ext",
        ),
    ]
    return instances
# </INGREDIENT>
