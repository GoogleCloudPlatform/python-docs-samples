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

from google.api_core.exceptions import BadRequest
from google.cloud import compute_v1


# <INGREDIENT create_disk_from_kms_encrypted_disk>
def create_disk_from_kms_encrypted_disk(
        project_id: str, zone: str, disk_name: str, disk_type: str,
        disk_size_gb: int, disk_link: str,
        kms_key_name: str) -> compute_v1.Disk:
    """
    Creates a zonal non-boot disk in a project with the copy of data from an existing disk.

    The encryption key must be the same for the source disk and the new disk.

    To run this method, the service-<project_id>@compute-system.iam.gserviceaccount.com
    service account needs to have the cloudkms.cryptoKeyEncrypterDecrypter role,
    as described in documentation:
    https://cloud.google.com/compute/docs/disks/customer-managed-encryption#before_you_begin

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone in which you want to create the disk.
        disk_name: name of the disk you want to create.
        disk_type: the type of disk you want to create. This value uses the following format:
            "zones/{zone}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "zones/us-west3-b/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        disk_link: a link to the disk you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/zones/{zone}/disks/{disk_name}"
        kms_key_name: URL of the key from KMS. The key might be from another project, as
            long as you have access to it. The data will be encrypted with the same key
            in the new disk. This value uses following format:
            "projects/{kms_project_id}/locations/{region}/keyRings/{key_ring}/cryptoKeys/{key}"

    Returns:
        An attachable copy of an existing disk.
    """
    disk_client = compute_v1.DisksClient()
    disk = compute_v1.Disk()
    disk.zone = zone
    disk.size_gb = disk_size_gb
    disk.source_disk = disk_link
    disk.type_ = disk_type
    disk.name = disk_name
    disk.disk_encryption_key = compute_v1.CustomerEncryptionKey()
    disk.disk_encryption_key.kms_key_name = kms_key_name
    try:
        operation = disk_client.insert(project=project_id, zone=zone, disk_resource=disk)
    except BadRequest as err:
        if "Permission 'cloudkms.cryptoKeyVersions.useToEncrypt' denied" in err.message:
            print(f"Please provide the cloudkms.cryptoKeyEncrypterDecrypter role to"
                  f"service-{project_id}@compute-system.iam.gserviceaccount.com")
        raise err

    wait_for_extended_operation(operation, "disk creation")

    return disk_client.get(project=project_id, zone=zone, disk=disk_name)
# </INGREDIENT>
