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
import time
import uuid

from google.api_core.exceptions import NotFound
import google.auth
from google.cloud import kms_v1
import pytest

from ..disks.attach_disk import attach_disk
from ..disks.clone_encrypted_disk_managed_key import \
    create_disk_from_kms_encrypted_disk
from ..disks.create_empty_disk import create_empty_disk
from ..disks.create_from_image import create_disk_from_image
from ..disks.create_from_source import create_disk_from_disk
from ..disks.create_kms_encrypted_disk import create_kms_encrypted_disk
from ..disks.delete import delete_disk
from ..disks.list import list_disks
from ..disks.regional_create_from_source import create_regional_disk
from ..disks.regional_delete import delete_regional_disk
from ..images.get import get_image_from_family
from ..instances.create import create_instance, disk_from_image
from ..instances.delete import delete_instance
from ..instances.get import get_instance
from ..snapshots.create import create_snapshot
from ..snapshots.delete import delete_snapshot

PROJECT = google.auth.default()[1]
ZONE = 'europe-central2-c'
REGION = 'europe-central2'
KMS_KEYRING_NAME = 'compute-test-keyring'
KMS_KEY_NAME = 'compute-test-key'


@pytest.fixture()
def kms_key():
    client = kms_v1.KeyManagementServiceClient()
    location = f"projects/{PROJECT}/locations/global"
    keyring_link = f"projects/{PROJECT}/locations/global/keyRings/{KMS_KEYRING_NAME}"
    key_name = f"{keyring_link}/cryptoKeys/{KMS_KEY_NAME}"

    for ring in client.list_key_rings(parent=location):
        if ring.name == keyring_link:
            break
    else:
        client.create_key_ring(parent=location, key_ring_id=KMS_KEYRING_NAME)

    for key in client.list_crypto_keys(parent=keyring_link):
        if key.name == key_name:
            break
    else:
        key = kms_v1.CryptoKey()
        key.purpose = key.CryptoKeyPurpose.ENCRYPT_DECRYPT
        client.create_crypto_key(parent=keyring_link, crypto_key_id=KMS_KEY_NAME, crypto_key=key)

    yield client.get_crypto_key(name=key_name)


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


@pytest.fixture()
def autodelete_disk_name():
    disk_name = "test-disk-" + uuid.uuid4().hex[:10]
    yield disk_name
    try:
        delete_disk(PROJECT, ZONE, disk_name)
    except NotFound:
        # The disk was already deleted
        pass


# To use the fixture 2 times in one test:
# https://stackoverflow.com/questions/36100624/pytest-use-same-fixture-twice-in-one-function
autodelete_disk_name2 = autodelete_disk_name


@pytest.fixture()
def autodelete_src_disk(autodelete_disk_name):
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    debian_image = get_image_from_family('debian-cloud', 'debian-11')
    disk = create_disk_from_image(PROJECT, ZONE, autodelete_disk_name, disk_type, 24, debian_image.self_link)
    yield disk


@pytest.fixture
def autodelete_instance_name():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]

    yield instance_name

    delete_instance(PROJECT, ZONE, instance_name)


@pytest.fixture
def autodelete_regional_blank_disk():
    disk_name = 'regional-disk-' + uuid.uuid4().hex[:10]
    replica_zones = [
        f"projects/{PROJECT}/zones/{REGION}-c",
        f"projects/{PROJECT}/zones/{REGION}-b",
    ]
    disk_type = f"regions/{REGION}/diskTypes/pd-balanced"

    disk = create_regional_disk(PROJECT, REGION, replica_zones, disk_name, disk_type, 11)

    yield disk

    try:
        # We wait for a while to let instances using this disk to be removed.
        time.sleep(60)
        delete_regional_disk(PROJECT, REGION, disk_name)
    except NotFound:
        # The disk was already deleted
        pass


@pytest.fixture
def autodelete_blank_disk():
    disk_name = 'regional-disk-' + uuid.uuid4().hex[:10]
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"

    disk = create_empty_disk(PROJECT, ZONE, disk_name, disk_type, 12)

    yield disk

    try:
        # We wait for a while to let instances using this disk to be removed.
        print('Waiting')
        time.sleep(60)
        print('Deleting')
        delete_disk(PROJECT, ZONE, disk_name)
    except NotFound:
        # The disk was already deleted
        pass


@pytest.fixture
def autodelete_compute_instance():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]
    newest_debian = get_image_from_family(project="ubuntu-os-cloud", family="ubuntu-2204-lts")
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 100, True, newest_debian.self_link)]
    instance = create_instance(
        PROJECT, ZONE, instance_name, disks
    )
    yield instance

    delete_instance(PROJECT, ZONE, instance_name)


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


def test_create_and_clone_encrypted_disk(autodelete_disk_name, kms_key, autodelete_disk_name2):
    # The service account service-{PROJECT_ID}@compute-system.iam.gserviceaccount.com needs to have the
    # cloudkms.cryptoKeyVersions.useToEncrypt permission to execute this test.
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    debian_image = get_image_from_family('debian-cloud', 'debian-11')

    disk = create_kms_encrypted_disk(PROJECT, ZONE, autodelete_disk_name, disk_type, 25, kms_key.name,
                                     image_link=debian_image.self_link)
    assert disk.name == autodelete_disk_name
    assert disk.type_.endswith(disk_type)

    disk2 = create_disk_from_kms_encrypted_disk(PROJECT, ZONE, autodelete_disk_name2, disk_type,
                                                25, disk_link=disk.self_link, kms_key_name=kms_key.name)
    assert disk2.name == autodelete_disk_name2
    assert disk2.type_.endswith(disk_type)


def test_create_disk_from_disk(autodelete_src_disk, autodelete_disk_name2):
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    new_disk = create_disk_from_disk(PROJECT, ZONE, autodelete_disk_name2, disk_type, 24, autodelete_src_disk.self_link)

    assert new_disk.type_.endswith(disk_type)
    assert new_disk.name == autodelete_disk_name2


def test_create_and_delete_regional_disk(test_snapshot):
    disk_name = "test-rdisk-" + uuid.uuid4().hex[:10]
    disk_type = f"regions/{REGION}/diskTypes/pd-balanced"
    replica_zones = [
        f"projects/{PROJECT}/zones/{REGION}-a",
        f"projects/{PROJECT}/zones/{REGION}-b",
    ]

    try:
        regional_disk = create_regional_disk(PROJECT, REGION, replica_zones, disk_name,
                                             disk_type, 25, snapshot_link=test_snapshot.self_link)
        assert regional_disk.name == disk_name
        assert regional_disk.type_.endswith(disk_type)
    finally:
        delete_regional_disk(PROJECT, REGION, disk_name)


def test_disk_attachment(autodelete_blank_disk, autodelete_regional_blank_disk, autodelete_compute_instance):
    instance = get_instance(PROJECT, ZONE, autodelete_compute_instance.name)

    assert len(list(instance.disks)) == 1

    attach_disk(PROJECT, ZONE, instance.name, autodelete_blank_disk.self_link)
    attach_disk(PROJECT, ZONE, instance.name, autodelete_regional_blank_disk.self_link)

    instance = get_instance(PROJECT, ZONE, autodelete_compute_instance.name)

    assert len(list(instance.disks)) == 3
