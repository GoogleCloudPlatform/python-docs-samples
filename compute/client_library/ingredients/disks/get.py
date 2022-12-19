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
import sys
from typing import NoReturn, Iterable

from google.cloud import compute_v1


# <INGREDIENT get_disk>
def get_disk(project_id: str, zone: str, disk_name: str) -> compute_v1.Disk:
    """
    Gets a disk from a project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone where the disk exists.
        disk_name: name of the disk you want to retrieve.
    """
    disk_client = compute_v1.DisksClient()
    return disk_client.get(project=project_id, zone=zone, disk=disk_name)
# </INGREDIENT>
