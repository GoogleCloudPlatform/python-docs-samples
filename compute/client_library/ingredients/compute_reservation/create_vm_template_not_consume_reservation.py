# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is an ingredient file. It is not meant to be run directly. Check the samples/snippets
# folder for complete code samples that are ready to be used.
# Disabling flake8 for the ingredients file, as it would fail F821 - undefined name check.
# flake8: noqa

from google.cloud import compute_v1

# <INGREDIENT create_template_not_consume_reservation>
def create_instance_template_not_consume_reservation(
    project_id: str,
    template_name: str,
    machine_type: str = "n1-standard-1",
) -> compute_v1.InstanceTemplate:
    """
    Creates an instance template that creates VMs that don't explicitly consume reservations

    Args:
        project_id: project ID or project number of the Cloud project you use.
        template_name: name of the new template to create.
        machine_type: machine type for the instance.
    Returns:
        InstanceTemplate object that represents the new instance template.
    """

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties.machine_type = machine_type
    # The template describes the size and source image of the boot disk
    # to attach to the instance.
    template.properties.disks = [
        compute_v1.AttachedDisk(
            boot=True,
            auto_delete=True,  # The disk will be deleted when the instance is deleted
            initialize_params=compute_v1.AttachedDiskInitializeParams(
                source_image="projects/debian-cloud/global/images/family/debian-11",
                disk_size_gb=10,
            ),
        )
    ]
    # The template connects the instance to the `default` network,
    template.properties.network_interfaces = [
        compute_v1.NetworkInterface(
            network="global/networks/default",
            access_configs=[
                compute_v1.AccessConfig(
                    name="External NAT",
                    type="ONE_TO_ONE_NAT",
                )
            ],
        )
    ]
    # The template doesn't explicitly consume reservations
    template.properties.reservation_affinity = compute_v1.ReservationAffinity(
        consume_reservation_type="NO_RESERVATION"
    )

    template_client = compute_v1.InstanceTemplatesClient()
    operation = template_client.insert(
        project=project_id, instance_template_resource=template
    )

    wait_for_extended_operation(operation, "instance template creation")

    return template_client.get(project=project_id, instance_template=template_name)
# </INGREDIENT>