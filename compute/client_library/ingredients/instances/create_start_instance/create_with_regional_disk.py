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


# <INGREDIENT create_with_regional_boot_disk>
def create_with_regional_boot_disk(
    project_id: str,
    zone: str,
    instance_name: str,
    source_snapshot: str,
    disk_region: str,
    disk_type: str = "pd-balanced",
) -> compute_v1.Instance:
    """
    Creates a new instance with a regional boot disk
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the instance will be created.
        instance_name (str): The name of the instance.
        source_snapshot (str): The name of snapshot to create the boot disk from.
        disk_region (str): The region where the disk replicas will be located.
        disk_type (str): The type of the disk. Default is 'pd-balanced'.
    Returns:
        Instance object.
    """

    disk = compute_v1.AttachedDisk()

    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_snapshot = f"global/snapshots/{source_snapshot}"
    initialize_params.disk_type = (
        f"projects/{project_id}/zones/{zone}/diskTypes/{disk_type}"
    )
    initialize_params.replica_zones = [
        f"projects/{project_id}/zones/{disk_region}-a",
        f"projects/{project_id}/zones/{disk_region}-b",
    ]

    disk.initialize_params = initialize_params
    disk.boot = True
    disk.auto_delete = True

    instance = create_instance(project_id, zone, instance_name, [disk])

    return instance


# </INGREDIENT>
