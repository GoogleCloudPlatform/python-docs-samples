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
from __future__ import annotations

from collections.abc import Iterable

from google.cloud import compute_v1


# <INGREDIENT list_disks>
def list_disks(
    project_id: str, zone: str, filter_: str = ""
) -> Iterable[compute_v1.Disk]:
    """
    Lists disks in a project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone
        filter_: filter to be applied when listing disks. Learn more about filters here:
            https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.types.ListDisksRequest
    """
    disk_client = compute_v1.DisksClient()
    request = compute_v1.ListDisksRequest()
    request.project = project_id
    request.zone = zone
    request.filter = filter_
    return disk_client.list(request)


# </INGREDIENT>
