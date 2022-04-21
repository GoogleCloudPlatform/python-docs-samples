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


# <INGREDIENT create_template_from_instance>
def create_template_from_instance(
    project_id: str, instance: str, template_name: str
) -> compute_v1.InstanceTemplate:
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
    disk.instantiate_from = "CUSTOM_IMAGE"
    disk.custom_image = "projects/rocky-linux-cloud/global/images/family/rocky-linux-8"
    # Override the auto_delete setting.
    disk.auto_delete = True

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.source_instance = instance
    template.source_instance_params = compute_v1.SourceInstanceParams()
    template.source_instance_params.disk_configs = [disk]

    template_client = compute_v1.InstanceTemplatesClient()
    operation = template_client.insert(
        project=project_id, instance_template_resource=template
    )

    wait_for_extended_operation(operation, "instance template creation")

    return template_client.get(project=project_id, instance_template=template_name)
# </INGREDIENT>
