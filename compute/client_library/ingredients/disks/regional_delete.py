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
from typing import NoReturn

from google.cloud import compute_v1


# <INGREDIENT delete_regional_disk>
def delete_regional_disk(project_id: str, region: str, disk_name: str) -> None:
    """
    Deletes a disk from a project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        region:name of the region where the disk is located.
        disk_name: name of the disk that you want to delete.
    """
    disk_client = compute_v1.RegionDisksClient()
    operation = disk_client.delete(project=project_id, region=region, disk=disk_name)
    wait_for_extended_operation(operation, "regional disk deletion")
# </INGREDIENT>
