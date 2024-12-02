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


# <INGREDIENT start_disk_replication>
def start_disk_replication(
    project_id: str,
    primary_disk_location: str,
    primary_disk_name: str,
    secondary_disk_location: str,
    secondary_disk_name: str,
) -> bool:
    """Starts the asynchronous replication of a primary disk to a secondary disk.
    Args:
        project_id (str): The ID of the Google Cloud project.
        primary_disk_location (str): The location of the primary disk, either a zone or a region.
        primary_disk_name (str): The name of the primary disk.
        secondary_disk_location (str): The location of the secondary disk, either a zone or a region.
        secondary_disk_name (str): The name of the secondary disk.
    Returns:
        bool: True if the replication was successfully started.
    """
    # Check if the primary disk location is a region or a zone.
    if primary_disk_location[-1].isdigit():
        region_client = compute_v1.RegionDisksClient()
        request_resource = compute_v1.RegionDisksStartAsyncReplicationRequest(
            async_secondary_disk=f"projects/{project_id}/regions/{secondary_disk_location}/disks/{secondary_disk_name}"
        )
        operation = region_client.start_async_replication(
            project=project_id,
            region=primary_disk_location,
            disk=primary_disk_name,
            region_disks_start_async_replication_request_resource=request_resource,
        )
    else:
        client = compute_v1.DisksClient()
        request_resource = compute_v1.DisksStartAsyncReplicationRequest(
            async_secondary_disk=f"zones/{secondary_disk_location}/disks/{secondary_disk_name}"
        )
        operation = client.start_async_replication(
            project=project_id,
            zone=primary_disk_location,
            disk=primary_disk_name,
            disks_start_async_replication_request_resource=request_resource,
        )
    wait_for_extended_operation(operation, verbose_name="replication operation")
    print(f"Replication for disk {primary_disk_name} started.")
    return True


# </INGREDIENT>
