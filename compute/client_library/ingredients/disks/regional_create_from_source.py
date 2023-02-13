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
from typing import Iterable, Optional

from google.cloud import compute_v1


# <INGREDIENT create_regional_disk_from_disk>
def create_regional_disk(project_id: str, region: str, replica_zones: Iterable[str],
                         disk_name: str, disk_type: str,
                         disk_size_gb: int,
                         disk_link: Optional[str] = None,
                         snapshot_link: Optional[str] = None) -> compute_v1.Disk:
    """
    Creates a regional disk from an existing zonal disk in a given project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region: name of the region in which you want to create the disk.
        replica_zones: an iterable collection of zone names in which you want to keep
            the new disks' replicas. One of the replica zones of the clone must match
            the zone of the source disk.
        disk_name: name of the disk you want to create.
        disk_type: the type of disk you want to create. This value uses the following format:
            "regions/{region}/diskTypes/(pd-standard|pd-ssd|pd-balanced|pd-extreme)".
            For example: "regions/us-west3/diskTypes/pd-ssd"
        disk_size_gb: size of the new disk in gigabytes
        disk_link: a link to the disk you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/zones/{zone}/disks/{disk_name}"
        snapshot_link: a link to the snapshot you want to use as a source for the new disk.
            This value uses the following format: "projects/{project_name}/global/snapshots/{snapshot_name}"

    Returns:
        An attachable regional disk.
    """
    disk_client = compute_v1.RegionDisksClient()
    disk = compute_v1.Disk()
    disk.replica_zones = replica_zones
    disk.size_gb = disk_size_gb
    if disk_link:
        disk.source_disk = disk_link
    if snapshot_link:
        disk.source_snapshot = snapshot_link
    disk.type_ = disk_type
    disk.region = region
    disk.name = disk_name
    operation = disk_client.insert(project=project_id, region=region, disk_resource=disk)

    wait_for_extended_operation(operation, "disk creation")

    return disk_client.get(project=project_id, region=region, disk=disk_name)
# </INGREDIENT>
