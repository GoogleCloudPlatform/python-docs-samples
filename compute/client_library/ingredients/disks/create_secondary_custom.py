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
# flake8: noqa

from google.cloud import compute_v1


# <INGREDIENT create_secondary_custom_disk>
def create_secondary_custom_disk(
    primary_disk_name: str,
    primary_disk_project: str,
    primary_disk_zone: str,
    secondary_disk_name: str,
    secondary_disk_project: str,
    secondary_disk_zone: str,
    disk_size_gb: int,
    disk_type: str = "pd-ssd",
) -> compute_v1.Disk:
    """Creates a custom secondary disk whose properties differ from the primary disk.
    Args:
        primary_disk_name (str): The name of the primary disk.
        primary_disk_project (str): The project of the primary disk.
        primary_disk_zone (str): The location of the primary disk.
        secondary_disk_name (str): The name of the secondary disk.
        secondary_disk_project (str): The project of the secondary disk.
        secondary_disk_zone (str): The location of the secondary disk.
        disk_size_gb (int): The size of the disk in GB. Should be the same as the primary disk.
        disk_type (str): The type of the disk. Must be one of pd-ssd or pd-balanced.
    """
    disk_client = compute_v1.DisksClient()
    disk = compute_v1.Disk()
    disk.name = secondary_disk_name
    disk.size_gb = disk_size_gb
    disk.type = f"zones/{primary_disk_zone}/diskTypes/{disk_type}"
    disk.async_primary_disk = compute_v1.DiskAsyncReplication(
        disk=f"projects/{primary_disk_project}/zones/{primary_disk_zone}/disks/{primary_disk_name}"
    )

    # Add guest OS features to the secondary dis
    # For possible values, visit:
    # https://cloud.google.com/compute/docs/images/create-custom#guest-os-features
    disk.guest_os_features = [compute_v1.GuestOsFeature(type="MULTI_IP_SUBNET")]

    # Assign additional labels to the secondary disk
    disk.labels = {
        "source-disk": primary_disk_name,
        "secondary-disk-for-replication": "true",
    }

    operation = disk_client.insert(
        project=secondary_disk_project, zone=secondary_disk_zone, disk_resource=disk
    )
    wait_for_extended_operation(operation, "create_secondary_disk")

    secondary_disk = disk_client.get(
        project=secondary_disk_project,
        zone=secondary_disk_zone,
        disk=secondary_disk_name,
    )
    return secondary_disk


# </INGREDIENT>
