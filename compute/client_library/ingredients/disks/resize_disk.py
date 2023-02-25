#  Copyright 2023 Google LLC
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
import re

from google.cloud import compute_v1


# <INGREDIENT resize_disk>
def resize_disk(project_id: str, disk_link: str, new_size_gb: int) -> None:
    """
    Resizes a persistent disk to a specified size in GB. After you resize the disk, you must
    also resize the file system so that the operating system can access the additional space.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        disk_link: a link to the disk you want to resize.
            This value uses the following format:
                * https://www.googleapis.com/compute/v1/projects/{project_name}/zones/{zone}/disks/{disk_name}
                * projects/{project_name}/zones/{zone}/disks/{disk_name}
                * projects/{project_name}/regions/{region}/disks/{disk_name}
        new_size_gb: the new size you want to set for the disk in gigabytes.
    """
    search_results = re.search(r"/projects/[\w_-]+/(?P<area_type>zones|regions)/"
                               r"(?P<area_name>[\w_-]+)/disks/(?P<disk_name>[\w_-]+)", disk_link)

    if search_results["area_type"] == "regions":
        disk_client = compute_v1.RegionDisksClient()
        request = compute_v1.ResizeRegionDiskRequest()
        request.region = search_results["area_name"]
        request.region_disks_resize_request_resource = compute_v1.RegionDisksResizeRequest()
        request.region_disks_resize_request_resource.size_gb = new_size_gb
    else:
        disk_client = compute_v1.DisksClient()
        request = compute_v1.ResizeDiskRequest()
        request.zone = search_results["area_name"]
        request.disks_resize_request_resource = compute_v1.DisksResizeRequest()
        request.disks_resize_request_resource.size_gb = new_size_gb

    request.disk = search_results["disk_name"]
    request.project = project_id

    operation = disk_client.resize(request)
    wait_for_extended_operation(operation, "disk resize")
# </INGREDIENT>
