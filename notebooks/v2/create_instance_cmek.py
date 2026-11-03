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

# [START notebooks_v2_create_instance_cmek]
import sys

from google.api_core import exceptions
from google.cloud import notebooks_v2


def create_instance_cmek(
    project_id: str,
    location_id: str = "us-central1-a",
    instance_id: str = "example-cmek-instance",
    key_ring_id: str = "example-key-ring",
    crypto_key_id: str = "example-key",
) -> None:
    """Creates a Workbench instance encrypted with a customer-managed key.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Compute Engine zone for the new instance.
        instance_id: The ID to assign to the new Workbench instance.
        key_ring_id: The Cloud KMS key ring ID in the instance region.
        crypto_key_id: The Cloud KMS crypto key ID used for disk encryption.
    """
    client = notebooks_v2.NotebookServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    parts = location_id.split("-")
    region_id = "-".join(parts[:-1]) if len(parts) > 2 else location_id
    kms_key = (
        f"projects/{project_id}/locations/{region_id}/"
        f"keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    )
    boot_disk = notebooks_v2.BootDisk(
        disk_size_gb=150,
        disk_type=notebooks_v2.DiskType.PD_SSD,
        disk_encryption=notebooks_v2.DiskEncryption.CMEK,
        kms_key=kms_key,
    )
    data_disk = notebooks_v2.DataDisk(
        disk_size_gb=100,
        disk_type=notebooks_v2.DiskType.PD_SSD,
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
        # The operation completes once the instance is accepted, before the
        # VM finishes provisioning, so the state is usually PROVISIONING here.
        response = operation.result()
        boot_encryption = response.gce_setup.boot_disk.disk_encryption.name
        print(f"Resource ID: {response.name}")
        print(f"Creation Date: {response.create_time}")
        print(f"Boot Disk Encryption: {boot_encryption}")
        print(f"State: {response.state.name}")
        print(
            "The instance is still starting up; call get_instance until the "
            "state is ACTIVE before connecting to JupyterLab."
        )
    except exceptions.AlreadyExists as err:
        print(
            f"error: Instance '{instance_id}' already exists in location "
            f"'{location_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )


# [END notebooks_v2_create_instance_cmek]
