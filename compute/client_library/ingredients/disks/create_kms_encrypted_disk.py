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
from typing import Optional

from google.cloud import compute_v1


# <INGREDIENT create_kms_encrypted_disk>
def create_kms_encrypted_disk(
        project_id: str,
        zone: str,
        disk_name: str,
        disk_type: str,
        disk_size_gb: int,
        kms_key_name: str,
        disk_link: Optional[str] = None,
        image_link: Optional[str] = None
) -> compute_v1.Disk:
    """
    Creates a zonal disk in a project. If you do not provide values for disk_link or image_link,
    an empty disk will be created.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which you want to create the disk.
        disk_name: name of the disk you want to create.
        disk_type: the type of disk you want to create. This value uses the following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        kms_key_name: URL of the key from KMS. The key might be from another project, as
            long as you have access to it. The data will be encrypted with the same key
            in the new disk. This value uses following format:
            "projects/{kms_project_id}/locations/{region}/keyRings/{key_ring}/cryptoKeys/{key}"
        disk_link: a link to the disk you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/zones/{zone}/disks/{disk_name}"
        image_link: a link to the image you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/global/images/{image_name}"

    Returns:
        An attachable disk.
    """
    disk_client = compute_v1.DisksClient()
    disk = compute_v1.Disk()
    disk.zone = zone
    disk.size_gb = disk_size_gb
    if disk_link:
        disk.source_disk = disk_link
    if image_link:
        disk.source_image = image_link
    disk.type_ = disk_type
    disk.name = disk_name
    disk.disk_encryption_key = compute_v1.CustomerEncryptionKey()
    disk.disk_encryption_key.kms_key_name = kms_key_name
    operation = disk_client.insert(project=project_id, zone=zone, disk_resource=disk)

    wait_for_extended_operation(operation, "disk creation")

    return disk_client.get(project=project_id, zone=zone, disk=disk_name)

# </INGREDIENT>
