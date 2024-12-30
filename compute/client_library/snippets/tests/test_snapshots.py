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

import google.auth
from google.cloud import compute_v1

import pytest

from ..disks.create_from_image import create_disk_from_image
from ..disks.delete import delete_disk
from ..images.get import get_image_from_family
from ..snapshots.create import create_snapshot
from ..snapshots.delete import delete_snapshot
from ..snapshots.get import get_snapshot
from ..snapshots.list import list_snapshots
from ..snapshots.schedule_attach_disk import snapshot_schedule_attach
from ..snapshots.schedule_create import snapshot_schedule_create
from ..snapshots.schedule_delete import snapshot_schedule_delete
from ..snapshots.schedule_get import snapshot_schedule_get
from ..snapshots.schedule_list import snapshot_schedule_list
from ..snapshots.schedule_remove_disk import snapshot_schedule_detach_disk
from ..snapshots.schedule_update import snapshot_schedule_update


PROJECT = google.auth.default()[1]
ZONE = "europe-west1-c"
REGION = "europe-west1"


@pytest.fixture
def test_disk():
    debian_image = get_image_from_family("debian-cloud", "debian-11")
    test_disk_name = "test-disk-" + uuid.uuid4().hex[:10]

    disk_type = f"zones/{ZONE}/diskTypes/pd-standard"

    disk = create_disk_from_image(
        PROJECT, ZONE, test_disk_name, disk_type, 20, debian_image.self_link
    )

    yield disk

    delete_disk(PROJECT, ZONE, test_disk_name)


@pytest.fixture
def test_schedule_snapshot():
    test_schedule_snapshot_name = "test-snapshot-" + uuid.uuid4().hex[:5]
    schedule_snapshot = snapshot_schedule_create(
        PROJECT,
        REGION,
        test_schedule_snapshot_name,
        "test description",
        {"env": "dev", "media": "images"},
    )
    yield schedule_snapshot
    snapshot_schedule_delete(PROJECT, REGION, test_schedule_snapshot_name)


def test_snapshot_create_delete(test_disk):
    snapshot_name = "test-snapshot-" + uuid.uuid4().hex[:10]
    snapshot = create_snapshot(PROJECT, test_disk.name, snapshot_name, zone=ZONE)
    assert snapshot.name == snapshot_name
    assert snapshot.source_disk == test_disk.self_link
    for i_snapshot in list_snapshots(PROJECT):
        if i_snapshot.name == snapshot_name:
            break
    else:
        pytest.fail("Couldn't find the created snapshot on snapshot list.")

    snapshot_get = get_snapshot(PROJECT, snapshot_name)
    assert snapshot_get.name == snapshot_name
    assert snapshot_get.disk_size_gb == snapshot.disk_size_gb
    assert snapshot_get.self_link == snapshot.self_link

    delete_snapshot(PROJECT, snapshot_name)
    for i_snapshot in list_snapshots(PROJECT):
        if i_snapshot.name == snapshot_name:
            pytest.fail(
                "Test snapshot found on snapshot list, while it should already be gone."
            )


def test_create_get_list_delete_schedule_snapshot():
    test_snapshot_name = "test-disk-" + uuid.uuid4().hex[:5]
    assert snapshot_schedule_create(
        PROJECT,
        REGION,
        test_snapshot_name,
        "test description",
        {"env": "dev", "media": "images"},
    )
    try:
        snapshot = snapshot_schedule_get(PROJECT, REGION, test_snapshot_name)
        assert snapshot.name == test_snapshot_name
        assert (
            snapshot.snapshot_schedule_policy.snapshot_properties.labels["env"] == "dev"
        )
        assert len(list(snapshot_schedule_list(PROJECT, REGION))) > 0
    finally:
        snapshot_schedule_delete(PROJECT, REGION, test_snapshot_name)
        assert len(list(snapshot_schedule_list(PROJECT, REGION))) == 0


def test_attach_disk_to_snapshot(test_schedule_snapshot, test_disk):
    snapshot_schedule_attach(
        PROJECT, ZONE, REGION, test_disk.name, test_schedule_snapshot.name
    )
    disk = compute_v1.DisksClient().get(project=PROJECT, zone=ZONE, disk=test_disk.name)
    assert test_schedule_snapshot.name in disk.resource_policies[0]


def test_remove_disk_from_snapshot(test_schedule_snapshot, test_disk):
    snapshot_schedule_attach(
        PROJECT, ZONE, REGION, test_disk.name, test_schedule_snapshot.name
    )
    snapshot_schedule_detach_disk(
        PROJECT, ZONE, REGION, test_disk.name, test_schedule_snapshot.name
    )
    disk = compute_v1.DisksClient().get(project=PROJECT, zone=ZONE, disk=test_disk.name)
    assert not disk.resource_policies


def test_update_schedule_snapshot(test_schedule_snapshot):
    new_labels = {"env": "prod", "media": "videos"}
    snapshot_schedule_update(
        project_id=PROJECT,
        region=REGION,
        schedule_name=test_schedule_snapshot.name,
        schedule_description="updated description",
        labels=new_labels,
    )
    snapshot = snapshot_schedule_get(PROJECT, REGION, test_schedule_snapshot.name)
    assert snapshot.snapshot_schedule_policy.snapshot_properties.labels["env"] == "prod"
