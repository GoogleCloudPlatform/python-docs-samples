#  Copyright 2024 Google LLC
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


# <INGREDIENT create_regional_instance_template>
def create_regional_instance_template(
    project_id: str, region: str, template_name: str
) -> compute_v1.InstanceTemplate:
    """Creates a regional instance template with the provided name and a specific instance configuration.
    Args:
        project_id (str): The ID of the Google Cloud project
        region (str, optional): The region where the instance template will be created.
        template_name (str): The name of the regional instance template.
    Returns:
        InstanceTemplate: The created instance template.
    """
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
    network_interface.network = f"projects/{project_id}/global/networks/default"

    # The template lets the instance use an external IP address.
    access_config = compute_v1.AccessConfig()
    access_config.name = "External NAT"  # Name of the access configuration.
    access_config.type_ = "ONE_TO_ONE_NAT"  # Type of the access configuration.
    access_config.network_tier = "PREMIUM"  # Network tier for the access configuration.

    network_interface.access_configs = [access_config]

    template = compute_v1.InstanceTemplate()
    template.name = template_name
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-4"
    template.properties.network_interfaces = [network_interface]

    # Create the instance template request in the specified region.
    request = compute_v1.InsertRegionInstanceTemplateRequest(
        instance_template_resource=template, project=project_id, region=region
    )

    client = compute_v1.RegionInstanceTemplatesClient()
    operation = client.insert(
        request=request,
    )
    wait_for_extended_operation(operation, "Instance template creation")

    template = client.get(
        project=project_id, region=region, instance_template=template_name
    )
    print(template.name)
    print(template.region)
    print(template.properties.disks[0].initialize_params.source_image)
    # Example response:
    # test-regional-template
    # https://www.googleapis.com/compute/v1/projects/[PROJECT_ID]/regions/[REGION]
    # projects/debian-cloud/global/images/family/debian-11

    return template


# </INGREDIENT>
