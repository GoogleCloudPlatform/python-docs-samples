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


# <INGREDIENT create_instance_from_template>
def create_instance_from_template(
    project_id: str, zone: str, instance_name: str, instance_template_url: str
) -> compute_v1.Instance:
    """
    Creates a Compute Engine VM instance from an instance template.

    Args:
        project_id: ID or number of the project you want to use.
        zone: Name of the zone you want to check, for example: us-west3-b
        instance_name: Name of the new instance.
        instance_template_url: URL of the instance template used for creating the new instance.
            It can be a full or partial URL.
            Examples:
            - https://www.googleapis.com/compute/v1/projects/project/global/instanceTemplates/example-instance-template
            - projects/project/global/instanceTemplates/example-instance-template
            - global/instanceTemplates/example-instance-template

    Returns:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()

    instance_insert_request = compute_v1.InsertInstanceRequest()
    instance_insert_request.project = project_id
    instance_insert_request.zone = zone
    instance_insert_request.source_instance_template = instance_template_url
    instance_insert_request.instance_resource.name = instance_name

    operation = instance_client.insert(instance_insert_request)
    wait_for_extended_operation(operation, "instance creation")

    return instance_client.get(project=project_id, zone=zone, instance=instance_name)
# </INGREDIENT>
