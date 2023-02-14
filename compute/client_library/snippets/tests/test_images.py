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
from ..images.create import create_image_from_disk
from ..images.create_from_image import create_image_from_image
from ..images.create_from_snapshot import create_image_from_snapshot
from ..images.delete import delete_image
from ..images.get import get_image
from ..images.get import get_image_from_family
from ..images.list import list_images
from ..images.set_deprecation_status import set_deprecation_status
from ..snapshots.create import create_snapshot
from ..snapshots.delete import delete_snapshot

PROJECT = google.auth.default()[1]
ZONE = 'europe-west2-c'


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


@pytest.fixture
def test_snapshot(test_disk):
    """
    Make a snapshot that will be deleted when tests are done.
    """
    test_snap_name = "test-snap-" + uuid.uuid4().hex[:10]
    snap = create_snapshot(PROJECT, test_disk.name, test_snap_name, zone=test_disk.zone.rsplit('/')[-1])
    yield snap
    delete_snapshot(PROJECT, snap.name)


@pytest.fixture
def autodelete_image_name():
    """
    Provide a name for an image that will be deleted after the test is done.
    """
    test_img_name = "test-img-" + uuid.uuid4().hex[:10]
    yield test_img_name

    delete_image(PROJECT, test_img_name)


@pytest.fixture()
def autodelete_image(autodelete_image_name):
    """
    An image that will be deleted after the test is done.
    """
    src_img = get_image_from_family('debian-cloud', 'debian-11')
    new_image = create_image_from_image(PROJECT, src_img.name, autodelete_image_name, 'debian-cloud',
                                        storage_location='eu')
    yield new_image


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

    assert image.name == image2.name


def test_create_delete_image(test_disk):
    test_image_name = "test-image-" + uuid.uuid4().hex[:10]
    new_image = create_image_from_disk(PROJECT, ZONE, test_disk.name, test_image_name)
    try:
        assert new_image.name == test_image_name
        assert new_image.disk_size_gb == 20
        assert isinstance(new_image, compute_v1.Image)
    finally:
        delete_image(PROJECT, test_image_name)

        for image in list_images(PROJECT):
            if image.name == test_image_name:
                pytest.fail(f"Image {test_image_name} should have been deleted.")


def test_image_from_image(autodelete_image_name):
    src_img = get_image_from_family('ubuntu-os-cloud', 'ubuntu-2204-lts')
    new_image = create_image_from_image(PROJECT, src_img.name, autodelete_image_name, 'ubuntu-os-cloud',
                                        guest_os_features=[compute_v1.GuestOsFeature.Type.MULTI_IP_SUBNET.name],
                                        storage_location='eu')

    assert new_image.storage_locations == ['eu']
    assert new_image.disk_size_gb == src_img.disk_size_gb
    assert new_image.name == autodelete_image_name
    assert any(feature.type_ == compute_v1.GuestOsFeature.Type.MULTI_IP_SUBNET.name for feature in new_image.guest_os_features)


def test_image_from_snapshot(test_snapshot, autodelete_image_name):
    img = create_image_from_snapshot(PROJECT, test_snapshot.name, autodelete_image_name,
                                     guest_os_features=[compute_v1.GuestOsFeature.Type.MULTI_IP_SUBNET.name],
                                     storage_location='us-central1')
    assert img.storage_locations == ['us-central1']
    assert img.name == autodelete_image_name
    assert any(
        feature.type_ == compute_v1.GuestOsFeature.Type.MULTI_IP_SUBNET.name for feature in img.guest_os_features)


def test_status_change(autodelete_image):
    set_deprecation_status(PROJECT, autodelete_image.name, compute_v1.DeprecationStatus.State.DEPRECATED)
    img = get_image(PROJECT, autodelete_image.name)
    assert img.name == autodelete_image.name
    assert img.deprecated.state == compute_v1.DeprecationStatus.State.DEPRECATED.name
