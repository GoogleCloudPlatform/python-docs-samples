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
from __future__ import annotations


from google.cloud import compute_v1


# <INGREDIENT create_windows_instance>
def create_windows_instance(project_id: str, zone: str, instance_name: str,
                            machine_type: str, source_image_family: str = "windows-2022",
                            network_link: str = "global/networks/default",
                            subnetwork_link: str | None = None) -> compute_v1.Instance:
    """
    Creates a new Windows Server instance that has only an internal IP address.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone to create the instance in. For example: "us-west3-b"
        instance_name: name of the new virtual machine (VM) instance.
        machine_type: machine type you want to create in following format:
            "zones/{zone}/machineTypes/{type_name}". For example:
            "zones/europe-west3-c/machineTypes/f1-micro"
            You can find the list of available machine types using:
            https://cloud.google.com/sdk/gcloud/reference/compute/machine-types/list
        source_image_family: name of the public image family for Windows Server or SQL Server images.
            https://cloud.google.com/compute/docs/images#os-compute-support
        network_link: name of the network you want the new instance to use.
            For example: "global/networks/default" represents the network
            named "default", which is created automatically for each project.
        subnetwork_link: name of the subnetwork you want the new instance to use.
            This value uses the following format:
           "regions/{region}/subnetworks/{subnetwork_name}"

    Returns:
        Instance object.
    """
    if subnetwork_link is None:
        subnetwork_link = f'regions/{zone}/subnetworks/default'

    base_image = get_image_from_family(
        project="windows-cloud", family=source_image_family
    )
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 100, True, base_image.self_link, True)]

    # You must verify or configure routes and firewall rules in your VPC network
    # to allow access to kms.windows.googlecloud.com.
    # More information about access to kms.windows.googlecloud.com: https://cloud.google.com/compute/docs/instances/windows/creating-managing-windows-instances#kms-server

    # Additionally, you must enable Private Google Access for subnets in your VPC network
    # that contain Windows instances with only internal IP addresses.
    # More information about Private Google Access: https://cloud.google.com/vpc/docs/configure-private-google-access#enabling

    instance = create_instance(
        project_id,
        zone,
        instance_name,
        disks,
        machine_type=machine_type,
        network_link=network_link,
        subnetwork_link=subnetwork_link,
        external_access=True,  # Set this to False to disable external IP for your instance
    )
    return instance
# </INGREDIENT>
