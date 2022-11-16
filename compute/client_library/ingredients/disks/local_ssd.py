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
from google.cloud import compute_v1


# <INGREDIENT local_ssd_disk>
def local_ssd_disk(zone: str) -> compute_v1.AttachedDisk():
    """
    Create an AttachedDisk object to be used in VM instance creation. The created disk contains
    no data and requires formatting before it can be used.

    Args:
        zone: The zone in which the local SSD drive will be attached.

    Returns:
        AttachedDisk object configured as a local SSD disk.
    """
    disk = compute_v1.AttachedDisk()
    disk.type_ = compute_v1.AttachedDisk.Type.SCRATCH.name
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.disk_type = f"zones/{zone}/diskTypes/local-ssd"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    return disk
# </INGREDIENT>
