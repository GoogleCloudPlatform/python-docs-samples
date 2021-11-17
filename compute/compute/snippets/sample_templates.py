# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START compute_template_list ]
from typing import Iterable
# [END compute_template_list ]

# [START compute_template_create ]
# [START compute_template_list ]
# [START compute_template_get ]
# [START compute_template_create_from_instance ]
# [START compute_template_create_with_subnet ]
# [START compute_template_delete ]
from google.cloud import compute_v1
# [END compute_template_delete ]
# [END compute_template_create_with_subnet ]
# [END compute_template_create_from_instance ]
# [END compute_template_get ]
# [END compute_template_list ]
# [END compute_template_create ]


# [START compute_template_get ]
def get_instance_template(project_id: str, template_name: str) -> compute_v1.InstanceTemplate:
    """
    Retrieve an instance template, which you can use to create virtual machine
    (VM) instances and managed instance groups (MIGs).

    Args:
        project_id: project ID or project number of the Cloud project you use.
        template_name: name of the template to retrieve.

    Returns:
        InstanceTemplate object that represents the retrieved template.
    """
    template_client = compute_v1.InstanceTemplatesClient()
    return template_client.get(project=project_id, instance_template=template_name)
# [END compute_template_get ]


# [START compute_template_list ]
def list_instance_templates(project_id: str) -> Iterable[compute_v1.InstanceTemplate]:
    """
    Get a list of InstanceTemplate objects available in a project.

    Args:
        project_id: project ID or project number of the Cloud project you use.

    Returns:
        Iterable list of InstanceTemplate objects.
    """
    template_client = compute_v1.InstanceTemplatesClient()
    return template_client.list(project=project_id)
# [END compute_template_list ]


# [START compute_template_create ]
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
    access_config.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT
    access_config.network_tier = (
        compute_v1.AccessConfig.NetworkTier.PREMIUM
    )
    network_interface.access_configs = [access_config]

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-4"
    template.properties.network_interfaces = [network_interface]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert(project=project_id, instance_template_resource=template)
    operation_client.wait(project=project_id, operation=op.name)

    return template_client.get(project=project_id, instance_template=template_name)
# [END compute_template_create ]


# [START compute_template_create_from_instance ]
def create_template_from_instance(project_id: str, instance: str, template_name: str) -> compute_v1.InstanceTemplate:
    """
    Create a new instance template based on an existing instance.
    This new template specifies a different boot disk.

    Args:
        project_id: project ID or project number of the Cloud project you use.
        instance: the instance to base the new template on. This value uses
            the following format: "projects/{project}/zones/{zone}/instances/{instance_name}"
        template_name: name of the new template to create.

    Returns:
        InstanceTemplate object that represents the new instance template.
    """
    disk = compute_v1.DiskInstantiationConfig()
    # Device name must match the name of a disk attached to the instance you are
    # basing your template on.
    disk.device_name = "disk-1"
    # Replace the original boot disk image used in your instance with a Rocky Linux image.
    disk.instantiate_from = (
        compute_v1.DiskInstantiationConfig.InstantiateFrom.CUSTOM_IMAGE
    )
    disk.custom_image = "projects/rocky-linux-cloud/global/images/family/rocky-linux-8"
    # Override the auto_delete setting.
    disk.auto_delete = True

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.source_instance = instance
    template.source_instance_params = compute_v1.SourceInstanceParams()
    template.source_instance_params.disk_configs = [disk]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert(project=project_id, instance_template_resource=template)
    operation_client.wait(project=project_id, operation=op.name)

    return template_client.get(project=project_id, instance_template=template_name)
# [END compute_template_create_from_instance ]


# [START compute_template_create_with_subnet ]
def create_template_with_subnet(
    project_id: str, network: str, subnetwork: str, template_name: str
) -> compute_v1.InstanceTemplate:
    """
    Create an instance template that uses a provided subnet.

    Args:
        project_id: project ID or project number of the Cloud project you use.
        network: the network to be used in the new template. This value uses
            the following format: "projects/{project}/global/networks/{network}"
        subnetwork: the subnetwork to be used in the new template. This value
            uses the following format: "projects/{project}/regions/{region}/subnetworks/{subnetwork}"
        template_name: name of the new template to create.

    Returns:
        InstanceTemplate object that represents the new instance template.
    """
    # The template describes the size and source image of the book disk to
    # attach to the instance.
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 250
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties = compute_v1.InstanceProperties()
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-4"

    # The template connects the instance to the specified network and subnetwork.
    network_interface = compute_v1.NetworkInterface()
    network_interface.network = network
    network_interface.subnetwork = subnetwork
    template.properties.network_interfaces = [network_interface]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert(project=project_id, instance_template_resource=template)
    operation_client.wait(project=project_id, operation=op.name)

    return template_client.get(project=project_id, instance_template=template_name)
# [END compute_template_create_with_subnet ]


# [START compute_template_delete ]
def delete_instance_template(project_id: str, template_name: str):
    """
    Delete an instance template.

    Args:
        project_id: project ID or project number of the Cloud project you use.
        template_name: name of the template to delete.
    """
    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.delete(project=project_id, instance_template=template_name)
    operation_client.wait(project=project_id, operation=op.name)
    return
# [END compute_template_delete ]
