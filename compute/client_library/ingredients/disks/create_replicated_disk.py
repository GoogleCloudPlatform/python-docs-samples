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


# <INGREDIENT create_replicated_disk>
def create_regional_replicated_disk(
    project_id,
    region,
    disk_name,
    size_gb,
    disk_type: str = "pd-ssd",
) -> compute_v1.Disk:
    """Creates a synchronously replicated disk in a region across two zones.
    Args:
        project_id (str): The ID of the Google Cloud project.
        region (str): The region where the disk will be created.
        disk_name (str): The name of the disk.
        size_gb (int): The size of the disk in gigabytes.
        disk_type (str): The type of the disk. Default is 'pd-ssd'.
    Returns:
        compute_v1.Disk: The created disk object.
    """
    disk = compute_v1.Disk()
    disk.name = disk_name

    # You can specify the zones where the disk will be replicated.
    disk.replica_zones = [
        f"zones/{region}-a",
        f"zones/{region}-b",
    ]
    disk.size_gb = size_gb
    disk.type = f"regions/{region}/diskTypes/{disk_type}"

    client = compute_v1.RegionDisksClient()
    operation = client.insert(project=project_id, region=region, disk_resource=disk)

    wait_for_extended_operation(operation, "Replicated disk creation")

    return client.get(project=project_id, region=region, disk=disk_name)


# </INGREDIENT>
