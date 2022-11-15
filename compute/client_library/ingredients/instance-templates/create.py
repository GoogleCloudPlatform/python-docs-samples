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
import sys

from google.cloud import compute_v1


# <INGREDIENT create_template>
def create_template(project_id: str, template_name: str) -> compute_v1.InstanceTemplate:
    """
    Create a new instance template with the provided name and a specific
    instance configuration.

    Args:
        project_id: project ID or project number of the Cloud project you use.
        template_name: name of the new template to create.

    Returns:
        InstanceTemplate object that represents the new instance template.
    """
    # The template describes the size and source image of the boot disk
    # to attach to the instance.
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 250
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    # The template connects the instance to the `default` network,
    # without specifying a subnetwork.
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"

    # The template lets the instance use an external IP address.
    access_config = compute_v1.AccessConfig()
    access_config.name = "External NAT"
    access_config.type_ = "ONE_TO_ONE_NAT"
    access_config.network_tier = "PREMIUM"
    network_interface.access_configs = [access_config]

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-4"
    template.properties.network_interfaces = [network_interface]

    template_client = compute_v1.InstanceTemplatesClient()
    operation = template_client.insert(
        project=project_id, instance_template_resource=template
    )

    wait_for_extended_operation(operation, "instance template creation")

    return template_client.get(project=project_id, instance_template=template_name)
# </INGREDIENT>
