# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import uuid

import google.auth
from google.cloud import compute_v1
import pytest

from ..disks.create_from_image import create_disk_from_image
from ..disks.delete import delete_disk
from ..images.create import create_image
from ..images.delete import delete_image
from ..images.get import get_image
from ..images.get import get_image_from_family
from ..images.list import list_images

PROJECT = google.auth.default()[1]
ZONE = 'europe-central2-c'


@pytest.fixture
def test_disk():
    """
    Get the newest version of debian 11 and make a disk from it.
    """
    new_debian = get_image_from_family('debian-cloud', 'debian-11')
    test_disk_name = "test-disk-" + uuid.uuid4().hex[:10]
    disk = create_disk_from_image(PROJECT, ZONE, test_disk_name,
                                  f"zones/{ZONE}/diskTypes/pd-standard",
                                  20, new_debian.self_link)
    yield disk
    delete_disk(PROJECT, ZONE, test_disk_name)


def test_list_images():
    images = list_images("debian-cloud")
    for img in images:
        assert img.kind == "compute#image"
        assert img.self_link.startswith(
            "https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/"
        )


def test_get_image():
    images = list_images("debian-cloud")
    image = next(iter(images))

    image2 = get_image("debian-cloud", image.name)

    assert image == image2


def test_create_delete_image(test_disk):
    test_image_name = "test-image-" + uuid.uuid4().hex[:10]
    new_image = create_image(PROJECT, ZONE, test_disk.name, test_image_name)
    try:
        assert new_image.name == test_image_name
        assert new_image.disk_size_gb == 20
        assert isinstance(new_image, compute_v1.Image)
    finally:
        delete_image(PROJECT, test_image_name)

        for image in list_images(PROJECT):
            if image.name == test_image_name:
                pytest.fail(f"Image {test_image_name} should have been deleted.")
