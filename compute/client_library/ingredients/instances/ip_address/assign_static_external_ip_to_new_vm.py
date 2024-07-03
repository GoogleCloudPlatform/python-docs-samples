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


# <INGREDIENT assign_static_external_ip_to_new_vm>
def assign_static_external_ip_to_new_vm(
    project_id: str, zone: str, instance_name: str, ip_address: str
) -> compute_v1.Instance:
    """
    Create a new VM instance with assigned static external IP address.

    Args:
        project_id (str): project ID or project number of the Cloud project you want to use.
        zone (str): name of the zone to create the instance in. For example: "us-west3-b"
        instance_name (str): name of the new virtual machine (VM) instance.
        ip_address(str): external address to be assigned to this instance. It must live in the same
        region as the zone of the instance and be precreated before function called.

    Returns:
        Instance object.
    """
    newest_debian = get_image_from_family(project="debian-cloud", family="debian-12")
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link, True)]
    instance = create_instance(
        project_id,
        zone,
        instance_name,
        disks,
        external_ipv4=ip_address,
        external_access=True,
    )
    return instance


# </INGREDIENT>
