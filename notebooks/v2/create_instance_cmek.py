# Copyright 2026 Google LLC
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

import argparse
import sys

# [START notebooks_v2_create_instance_cmek]
from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_cmek(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-cmek-instance",
    key_ring_id: str = "example-key-ring",
    crypto_key_id: str = "example-key",
) -> None:
    """Creates a CMEK-encrypted Workbench instance.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
        key_ring_id: The Cloud KMS key ring ID in the same region.
        crypto_key_id: The Cloud KMS crypto key ID used for disk encryption.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    region_id = "-".join(location_id.split("-")[:-1])
    kms_key = (
        f"projects/{project_id}/locations/{region_id}/"
        f"keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    )
    boot_disk = notebooks_v2.BootDisk(
        disk_size_gb=150,
        disk_encryption=notebooks_v2.DiskEncryption.CMEK,
        kms_key=kms_key,
    )
    data_disk = notebooks_v2.DataDisk(
        disk_size_gb=100,
        disk_encryption=notebooks_v2.DiskEncryption.CMEK,
        kms_key=kms_key,
    )
    gce_setup = notebooks_v2.GceSetup(
        machine_type="e2-standard-4",
        boot_disk=boot_disk,
        data_disks=[data_disk],
    )
    instance = notebooks_v2.Instance(gce_setup=gce_setup)
    request = notebooks_v2.CreateInstanceRequest(
        parent=parent,
        instance_id=instance_id,
        instance=instance,
    )

    try:
        operation = client.create_instance(request=request)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        response = operation.result()
        encryption = response.gce_setup.boot_disk.disk_encryption.name
        print(f"Resource ID: {response.name}")
        print(f"Boot Disk Encryption: {encryption}")
        print(f"KMS Key: {response.gce_setup.boot_disk.kms_key}")
        print(f"State: {response.state.name}")
    except exceptions.AlreadyExists as err:
        print(
            f"error: Instance '{instance_id}' already exists in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_create_instance_cmek]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a CMEK-encrypted Workbench instance."
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="The Google Cloud project ID.",
    )
    parser.add_argument(
        "--location-id",
        default="us-central1-a",
        help="The Compute Engine zone.",
    )
    parser.add_argument(
        "--instance-id",
        default="example-cmek-instance",
        help="The ID for the new Workbench instance.",
    )
    parser.add_argument(
        "--key-ring-id",
        default="example-key-ring",
        help="The Cloud KMS key ring ID.",
    )
    parser.add_argument(
        "--crypto-key-id",
        default="example-key",
        help="The Cloud KMS crypto key ID.",
    )
    args = parser.parse_args()
    create_instance_cmek(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
        key_ring_id=args.key_ring_id,
        crypto_key_id=args.crypto_key_id,
    )
