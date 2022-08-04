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
import uuid

from google.api_core.exceptions import NotFound
import google.auth
import pytest

from ..disks.create_from_image import create_disk_from_image
from ..disks.delete import delete_disk
from ..disks.list import list_disks
from ..images.get import get_image_from_family

PROJECT = google.auth.default()[1]
ZONE = 'europe-north1-c'


@pytest.fixture()
def autodelete_disk_name():
    disk_name = "test-disk-" + uuid.uuid4().hex[:10]
    yield disk_name
    try:
        delete_disk(PROJECT, ZONE, disk_name)
    except NotFound:
        # The disk was already deleted
        pass


def test_disk_create_delete(autodelete_disk_name):
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    debian_image = get_image_from_family('debian-cloud', 'debian-11')

    disk = create_disk_from_image(PROJECT, ZONE, autodelete_disk_name, disk_type, 17, debian_image.self_link)
    assert disk.name == autodelete_disk_name
    assert disk.type_.endswith(disk_type)
    assert disk.size_gb == 17

    for i_disk in list_disks(PROJECT, ZONE):
        if i_disk.name == autodelete_disk_name:
            break
    else:
        pytest.fail("Couldn't find newly created disk on the disk list.")

    delete_disk(PROJECT, ZONE, autodelete_disk_name)

    for i_disk in list_disks(PROJECT, ZONE):
        if i_disk.name == autodelete_disk_name:
            pytest.fail("Found a disk that should be deleted on the disk list.")
