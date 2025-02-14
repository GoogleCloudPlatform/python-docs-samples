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
from google.cloud import compute_v1, kms_v1

import pytest

from ..disks.attach_disk import attach_disk
from ..disks.attach_regional_disk_force import attach_disk_force
from ..disks.attach_regional_disk_to_vm import attach_regional_disk
from ..disks.clone_encrypted_disk_managed_key import create_disk_from_kms_encrypted_disk
from ..disks.consistency_groups.add_disk_consistency_group import (
    add_disk_consistency_group,
)
from ..disks.consistency_groups.clone_disks_consistency_group import (
    clone_disks_to_consistency_group,
)
from ..disks.consistency_groups.create_consistency_group import create_consistency_group
from ..disks.consistency_groups.delete_consistency_group import delete_consistency_group
from ..disks.consistency_groups.remove_disk_consistency_group import (
    remove_disk_consistency_group,
)
from ..disks.consistency_groups.stop_replication_consistency_group import (
    stop_replication_consistency_group,
)
from ..disks.create_empty_disk import create_empty_disk
from ..disks.create_from_image import create_disk_from_image
from ..disks.create_from_source import create_disk_from_disk
from ..disks.create_hyperdisk import create_hyperdisk
from ..disks.create_hyperdisk_from_pool import create_hyperdisk_from_pool
from ..disks.create_hyperdisk_storage_pool import create_hyperdisk_storage_pool
from ..disks.create_kms_encrypted_disk import create_kms_encrypted_disk
from ..disks.create_replicated_disk import create_regional_replicated_disk
from ..disks.create_secondary_custom import create_secondary_custom_disk
from ..disks.create_secondary_disk import create_secondary_disk
from ..disks.create_secondary_region_disk import create_secondary_region_disk

from ..disks.delete import delete_disk
from ..disks.list import list_disks
from ..disks.regional_create_from_source import create_regional_disk
from ..disks.regional_delete import delete_regional_disk
from ..disks.replication_disk_start import start_disk_replication
from ..disks.replication_disk_stop import stop_disk_replication
from ..disks.resize_disk import resize_disk
from ..images.get import get_image_from_family
from ..instances.create import create_instance, disk_from_image
from ..instances.delete import delete_instance
from ..instances.get import get_instance
from ..snapshots.create import create_snapshot
from ..snapshots.delete import delete_snapshot

PROJECT = google.auth.default()[1]
ZONE = "europe-west2-c"
ZONE_SECONDARY = "europe-west1-c"
REGION = "europe-west2"
REGION_SECONDARY = "europe-west3"
KMS_KEYRING_NAME = "compute-test-keyring"
KMS_KEY_NAME = "compute-test-key"
DISK_SIZE = 15


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
        client.create_crypto_key(
            parent=keyring_link, crypto_key_id=KMS_KEY_NAME, crypto_key=key
        )

    yield client.get_crypto_key(name=key_name)


@pytest.fixture
def test_disk():
    """
    Get the newest version of debian 11 and make a disk from it.
    """
    new_debian = get_image_from_family("debian-cloud", "debian-11")
    test_disk_name = "test-disk-" + uuid.uuid4().hex[:10]
    disk = create_disk_from_image(
        PROJECT,
        ZONE,
        test_disk_name,
        f"zones/{ZONE}/diskTypes/pd-standard",
        20,
        new_debian.self_link,
    )
    yield disk
    delete_disk(PROJECT, ZONE, test_disk_name)


@pytest.fixture
def test_empty_pd_balanced_disk():
    """
    Creates and deletes a pd_balanced disk in secondary zone.
    """
    disk_name = "test-pd-balanced-disk" + uuid.uuid4().hex[:4]
    disk = create_empty_disk(
        PROJECT,
        ZONE_SECONDARY,
        disk_name,
        f"zones/{ZONE_SECONDARY}/diskTypes/pd-balanced",
        disk_size_gb=DISK_SIZE,
    )
    yield disk
    delete_disk(PROJECT, ZONE_SECONDARY, disk_name)


@pytest.fixture
def test_snapshot(test_disk):
    """
    Make a snapshot that will be deleted when tests are done.
    """
    test_snap_name = "test-snap-" + uuid.uuid4().hex[:10]
    snap = create_snapshot(
        PROJECT, test_disk.name, test_snap_name, zone=test_disk.zone.rsplit("/")[-1]
    )
    yield snap
    delete_snapshot(PROJECT, snap.name)


@pytest.fixture()
def autodelete_regional_disk_name():
    disk_name = "secondary-region-disk" + uuid.uuid4().hex[:4]
    yield disk_name
    try:
        delete_regional_disk(PROJECT, REGION_SECONDARY, disk_name)
    except NotFound:
        # The disk was already deleted
        pass


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
    debian_image = get_image_from_family("debian-cloud", "debian-11")
    disk = create_disk_from_image(
        PROJECT, ZONE, autodelete_disk_name, disk_type, 24, debian_image.self_link
    )
    yield disk


@pytest.fixture
def autodelete_instance_name():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]

    yield instance_name

    delete_instance(PROJECT, ZONE, instance_name)


@pytest.fixture
def autodelete_regional_blank_disk():
    disk_name = "regional-disk-" + uuid.uuid4().hex[:10]
    replica_zones = [
        f"projects/{PROJECT}/zones/{REGION}-c",
        f"projects/{PROJECT}/zones/{REGION}-b",
    ]
    disk_type = f"regions/{REGION}/diskTypes/pd-balanced"

    disk = create_regional_disk(
        PROJECT, REGION, replica_zones, disk_name, disk_type, DISK_SIZE
    )

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
    disk_name = "test-disk-" + uuid.uuid4().hex[:10]
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"

    disk = create_empty_disk(PROJECT, ZONE, disk_name, disk_type, 12)

    yield disk

    try:
        # We wait for a while to let instances using this disk to be removed.
        print("Waiting")
        time.sleep(60)
        print("Deleting")
        delete_disk(PROJECT, ZONE, disk_name)
    except NotFound:
        # The disk was already deleted
        pass


@pytest.fixture
def autodelete_compute_instance():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]
    newest_debian = get_image_from_family(
        project="ubuntu-os-cloud", family="ubuntu-2204-lts"
    )
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 100, True, newest_debian.self_link)]
    instance = create_instance(PROJECT, ZONE, instance_name, disks)
    yield instance

    delete_instance(PROJECT, ZONE, instance_name)


@pytest.fixture(scope="session")
def autodelete_hyperdisk_pool():
    pool_name = "test-pool-" + uuid.uuid4().hex[:6]
    pool = create_hyperdisk_storage_pool(PROJECT, ZONE, pool_name)
    yield pool
    pool_client = compute_v1.StoragePoolsClient()
    pool_client.delete(project=PROJECT, zone=ZONE, storage_pool=pool_name)


def test_disk_create_delete(autodelete_disk_name):
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    debian_image = get_image_from_family("debian-cloud", "debian-11")

    disk = create_disk_from_image(
        PROJECT, ZONE, autodelete_disk_name, disk_type, 17, debian_image.self_link
    )
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


def test_create_and_clone_encrypted_disk(
    autodelete_disk_name, kms_key, autodelete_disk_name2
):
    # The service account service-{PROJECT_ID}@compute-system.iam.gserviceaccount.com needs to have the
    # cloudkms.cryptoKeyVersions.useToEncrypt permission to execute this test.
    # Best way is to give this account the cloudkms.cryptoKeyEncrypterDecrypter role.
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    debian_image = get_image_from_family("debian-cloud", "debian-11")

    disk = create_kms_encrypted_disk(
        PROJECT,
        ZONE,
        autodelete_disk_name,
        disk_type,
        25,
        kms_key.name,
        image_link=debian_image.self_link,
    )
    assert disk.name == autodelete_disk_name
    assert disk.type_.endswith(disk_type)

    disk2 = create_disk_from_kms_encrypted_disk(
        PROJECT,
        ZONE,
        autodelete_disk_name2,
        disk_type,
        25,
        disk_link=disk.self_link,
        kms_key_name=kms_key.name,
    )
    assert disk2.name == autodelete_disk_name2
    assert disk2.type_.endswith(disk_type)


def test_create_disk_from_disk(autodelete_src_disk, autodelete_disk_name2):
    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    new_disk = create_disk_from_disk(
        PROJECT,
        ZONE,
        autodelete_disk_name2,
        disk_type,
        24,
        autodelete_src_disk.self_link,
    )

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
        regional_disk = create_regional_disk(
            PROJECT,
            REGION,
            replica_zones,
            disk_name,
            disk_type,
            25,
            snapshot_link=test_snapshot.self_link,
        )
        assert regional_disk.name == disk_name
        assert regional_disk.type_.endswith(disk_type)
    finally:
        delete_regional_disk(PROJECT, REGION, disk_name)


def test_disk_attachment(
    autodelete_blank_disk, autodelete_regional_blank_disk, autodelete_compute_instance
):
    instance = get_instance(PROJECT, ZONE, autodelete_compute_instance.name)

    assert len(list(instance.disks)) == 1

    attach_disk(
        PROJECT, ZONE, instance.name, autodelete_blank_disk.self_link, "READ_ONLY"
    )
    attach_disk(
        PROJECT,
        ZONE,
        instance.name,
        autodelete_regional_blank_disk.self_link,
        "READ_WRITE",
    )

    instance = get_instance(PROJECT, ZONE, autodelete_compute_instance.name)

    assert len(list(instance.disks)) == 3


def test_regional_disk_force_attachment(
    autodelete_regional_blank_disk, autodelete_compute_instance
):
    attach_disk_force(
        project_id=PROJECT,
        vm_name=autodelete_compute_instance.name,
        vm_zone=ZONE,
        disk_name=autodelete_regional_blank_disk.name,
        disk_region=REGION,
    )

    instance = get_instance(PROJECT, ZONE, autodelete_compute_instance.name)
    assert any(
        [autodelete_regional_blank_disk.name in disk.source for disk in instance.disks]
    )


def test_disk_resize(autodelete_blank_disk, autodelete_regional_blank_disk):
    resize_disk(PROJECT, autodelete_blank_disk.self_link, 22)
    resize_disk(PROJECT, autodelete_regional_blank_disk.self_link, 23)

    disk_client = compute_v1.DisksClient()
    regional_disk_client = compute_v1.RegionDisksClient()
    assert (
        disk_client.get(
            project=PROJECT, zone=ZONE, disk=autodelete_blank_disk.name
        ).size_gb
        == 22
    )
    assert (
        regional_disk_client.get(
            project=PROJECT, region=REGION, disk=autodelete_regional_blank_disk.name
        ).size_gb
        == 23
    )


def test_create_hyperdisk_pool(autodelete_hyperdisk_pool):
    assert "hyperdisk" in autodelete_hyperdisk_pool.storage_pool_type


def test_create_hyperdisk_from_pool(autodelete_hyperdisk_pool, autodelete_disk_name):
    disk = create_hyperdisk_from_pool(
        PROJECT, ZONE, autodelete_disk_name, autodelete_hyperdisk_pool.name
    )
    assert disk.storage_pool == autodelete_hyperdisk_pool.self_link
    assert "hyperdisk" in disk.type


def test_create_hyperdisk(autodelete_disk_name):
    disk = create_hyperdisk(PROJECT, ZONE, autodelete_disk_name, 100)
    assert "hyperdisk" in disk.type_.lower()


def test_create_secondary_region(
    autodelete_regional_blank_disk, autodelete_regional_disk_name
):
    disk = create_secondary_region_disk(
        autodelete_regional_blank_disk.name,
        PROJECT,
        REGION,
        autodelete_regional_disk_name,
        PROJECT,
        REGION_SECONDARY,
        DISK_SIZE,
    )
    assert disk.async_primary_disk.disk == autodelete_regional_blank_disk.self_link


def test_create_secondary(test_empty_pd_balanced_disk, autodelete_disk_name):
    disk = create_secondary_disk(
        primary_disk_name=test_empty_pd_balanced_disk.name,
        primary_disk_project=PROJECT,
        primary_disk_zone=ZONE_SECONDARY,
        secondary_disk_name=autodelete_disk_name,
        secondary_disk_project=PROJECT,
        secondary_disk_zone=ZONE,
        disk_size_gb=DISK_SIZE,
        disk_type="pd-ssd",
    )
    assert disk.async_primary_disk.disk == test_empty_pd_balanced_disk.self_link


def test_create_custom_secondary_disk(
    test_empty_pd_balanced_disk, autodelete_disk_name
):
    disk = create_secondary_custom_disk(
        primary_disk_name=test_empty_pd_balanced_disk.name,
        primary_disk_project=PROJECT,
        primary_disk_zone=ZONE_SECONDARY,
        secondary_disk_name=autodelete_disk_name,
        secondary_disk_project=PROJECT,
        secondary_disk_zone=ZONE,
        disk_size_gb=DISK_SIZE,
        disk_type="pd-ssd",
    )
    assert disk.labels["secondary-disk-for-replication"] == "true"
    assert disk.labels["source-disk"] == test_empty_pd_balanced_disk.name


def test_create_replicated_disk(autodelete_regional_disk_name):
    disk = create_regional_replicated_disk(
        project_id=PROJECT,
        region=REGION_SECONDARY,
        disk_name=autodelete_regional_disk_name,
        size_gb=DISK_SIZE,
    )
    assert f"{PROJECT}/zones/{REGION_SECONDARY}-" in disk.replica_zones[0]
    assert f"{PROJECT}/zones/{REGION_SECONDARY}-" in disk.replica_zones[1]


def test_start_stop_region_replication(
    autodelete_regional_blank_disk, autodelete_regional_disk_name
):
    create_secondary_region_disk(
        autodelete_regional_blank_disk.name,
        PROJECT,
        REGION,
        autodelete_regional_disk_name,
        PROJECT,
        REGION_SECONDARY,
        DISK_SIZE,
    )
    assert start_disk_replication(
        project_id=PROJECT,
        primary_disk_location=REGION,
        primary_disk_name=autodelete_regional_blank_disk.name,
        secondary_disk_location=REGION_SECONDARY,
        secondary_disk_name=autodelete_regional_disk_name,
    )
    assert stop_disk_replication(
        project_id=PROJECT,
        primary_disk_location=REGION,
        primary_disk_name=autodelete_regional_blank_disk.name,
    )
    # Wait for the replication to stop
    time.sleep(20)


def test_start_stop_zone_replication(test_empty_pd_balanced_disk, autodelete_disk_name):
    create_secondary_disk(
        test_empty_pd_balanced_disk.name,
        PROJECT,
        ZONE_SECONDARY,
        autodelete_disk_name,
        PROJECT,
        ZONE,
        DISK_SIZE,
    )
    assert start_disk_replication(
        project_id=PROJECT,
        primary_disk_location=ZONE_SECONDARY,
        primary_disk_name=test_empty_pd_balanced_disk.name,
        secondary_disk_location=ZONE,
        secondary_disk_name=autodelete_disk_name,
    )
    assert stop_disk_replication(
        project_id=PROJECT,
        primary_disk_location=ZONE_SECONDARY,
        primary_disk_name=test_empty_pd_balanced_disk.name,
    )
    # Wait for the replication to stop
    time.sleep(20)


def test_attach_regional_disk_to_vm(
    autodelete_regional_blank_disk, autodelete_compute_instance
):
    attach_regional_disk(
        PROJECT,
        ZONE,
        autodelete_compute_instance.name,
        REGION,
        autodelete_regional_blank_disk.name,
    )

    instance = get_instance(PROJECT, ZONE, autodelete_compute_instance.name)
    assert len(list(instance.disks)) == 2


def test_clone_disks_in_consistency_group(
    autodelete_regional_disk_name,
    autodelete_regional_blank_disk,
):
    group_name1 = "first-group" + uuid.uuid4().hex[:5]
    group_name2 = "second-group" + uuid.uuid4().hex[:5]
    create_consistency_group(PROJECT, REGION, group_name1, "description")
    create_consistency_group(PROJECT, REGION_SECONDARY, group_name2, "description")

    add_disk_consistency_group(
        project_id=PROJECT,
        disk_name=autodelete_regional_blank_disk.name,
        disk_location=REGION,
        consistency_group_name=group_name1,
        consistency_group_region=REGION,
    )

    second_disk = create_secondary_region_disk(
        autodelete_regional_blank_disk.name,
        PROJECT,
        REGION,
        autodelete_regional_disk_name,
        PROJECT,
        REGION_SECONDARY,
        DISK_SIZE,
    )

    add_disk_consistency_group(
        project_id=PROJECT,
        disk_name=second_disk.name,
        disk_location=REGION_SECONDARY,
        consistency_group_name=group_name2,
        consistency_group_region=REGION_SECONDARY,
    )

    start_disk_replication(
        project_id=PROJECT,
        primary_disk_location=REGION,
        primary_disk_name=autodelete_regional_blank_disk.name,
        secondary_disk_location=REGION_SECONDARY,
        secondary_disk_name=autodelete_regional_disk_name,
    )
    time.sleep(70)
    try:
        assert clone_disks_to_consistency_group(PROJECT, REGION_SECONDARY, group_name2)
    finally:
        stop_disk_replication(
            project_id=PROJECT,
            primary_disk_location=REGION,
            primary_disk_name=autodelete_regional_blank_disk.name,
        )
        # Wait for the replication to stop
        time.sleep(45)
        disks = compute_v1.RegionDisksClient().list(
            project=PROJECT, region=REGION_SECONDARY
        )
        if disks:
            for disk in disks:
                delete_regional_disk(PROJECT, REGION_SECONDARY, disk.name)
        time.sleep(30)
        remove_disk_consistency_group(
            PROJECT, autodelete_regional_blank_disk.name, REGION, group_name1, REGION
        )
        delete_consistency_group(PROJECT, REGION, group_name1)
        delete_consistency_group(PROJECT, REGION_SECONDARY, group_name2)


def test_stop_replications_in_consistency_group(
    autodelete_regional_blank_disk, autodelete_regional_disk_name
):
    group_name = "test-consistency-group" + uuid.uuid4().hex[:5]
    create_consistency_group(PROJECT, REGION, group_name, "description")
    add_disk_consistency_group(
        project_id=PROJECT,
        disk_name=autodelete_regional_blank_disk.name,
        disk_location=REGION,
        consistency_group_name=group_name,
        consistency_group_region=REGION,
    )
    second_disk = create_secondary_region_disk(
        autodelete_regional_blank_disk.name,
        PROJECT,
        REGION,
        autodelete_regional_disk_name,
        PROJECT,
        REGION_SECONDARY,
        DISK_SIZE,
    )
    start_disk_replication(
        project_id=PROJECT,
        primary_disk_location=REGION,
        primary_disk_name=autodelete_regional_blank_disk.name,
        secondary_disk_location=REGION_SECONDARY,
        secondary_disk_name=second_disk.name,
    )
    time.sleep(15)
    try:
        assert stop_replication_consistency_group(PROJECT, REGION, group_name)
    finally:
        remove_disk_consistency_group(
            project_id=PROJECT,
            disk_name=autodelete_regional_blank_disk.name,
            disk_location=REGION,
            consistency_group_name=group_name,
            consistency_group_region=REGION,
        )
        time.sleep(10)
        delete_consistency_group(PROJECT, REGION, group_name)
