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

from ..instances.create_start_instance.create_from_custom_image import (
    create_from_custom_image,
)
from ..instances.create_start_instance.create_from_public_image import (
    create_from_public_image,
)
from ..instances.create_start_instance.create_from_snapshot import create_from_snapshot
from ..instances.create_start_instance.create_with_additional_disk import (
    create_with_additional_disk,
)
from ..instances.create_start_instance.create_with_snapshotted_data_disk import (
    create_with_snapshotted_data_disk,
)
from ..instances.create_with_subnet import create_with_subnet
from ..instances.delete import delete_instance
from ..operations.operation_check import wait_for_operation

PROJECT = google.auth.default()[1]
REGION = "us-central1"
INSTANCE_ZONE = "us-central1-b"


def get_active_debian():
    image_client = compute_v1.ImagesClient()

    return image_client.get_from_family(project="debian-cloud", family="debian-11")


@pytest.fixture()
def src_disk():
    disk_client = compute_v1.DisksClient()

    disk = compute_v1.Disk()
    disk.source_image = get_active_debian().self_link
    disk.name = "test-disk-" + uuid.uuid4().hex[:10]
    op = disk_client.insert_unary(
        project=PROJECT, zone=INSTANCE_ZONE, disk_resource=disk
    )

    wait_for_operation(op, PROJECT)
    try:
        disk = disk_client.get(project=PROJECT, zone=INSTANCE_ZONE, disk=disk.name)
        yield disk
    finally:
        op = disk_client.delete_unary(
            project=PROJECT, zone=INSTANCE_ZONE, disk=disk.name
        )
        wait_for_operation(op, PROJECT)


@pytest.fixture()
def snapshot(src_disk):
    snapshot_client = compute_v1.SnapshotsClient()
    snapshot = compute_v1.Snapshot()
    snapshot.name = "test-snap-" + uuid.uuid4().hex[:10]
    disk_client = compute_v1.DisksClient()
    op = disk_client.create_snapshot_unary(
        project=PROJECT,
        zone=INSTANCE_ZONE,
        disk=src_disk.name,
        snapshot_resource=snapshot,
    )
    wait_for_operation(op, PROJECT)
    try:
        snapshot = snapshot_client.get(
            project=PROJECT, snapshot=snapshot.name
        )

        yield snapshot
    finally:
        op = snapshot_client.delete_unary(project=PROJECT, snapshot=snapshot.name)
        wait_for_operation(op, PROJECT)


@pytest.fixture()
def image(src_disk):
    image_client = compute_v1.ImagesClient()
    image = compute_v1.Image()
    image.source_disk = src_disk.self_link
    image.name = "test-image-" + uuid.uuid4().hex[:10]
    op = image_client.insert_unary(project=PROJECT, image_resource=image)

    wait_for_operation(op, PROJECT)
    try:
        image = image_client.get(project=PROJECT, image=image.name)
        yield image
    finally:
        op = image_client.delete_unary(project=PROJECT, image=image.name)
        wait_for_operation(op, PROJECT)


class TestCreation:
    def test_create_from_custom_image(self, image):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_from_custom_image(
            PROJECT, INSTANCE_ZONE, instance_name, image.self_link
        )
        try:
            assert (
                instance.disks[0].initialize_params.source_image == image.self_link
            )
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_from_public_image(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_from_public_image(
            PROJECT,
            INSTANCE_ZONE,
            instance_name,
        )
        try:
            assert "debian-cloud" in instance.disks[0].initialize_params.source_image
            assert "debian-10" in instance.disks[0].initialize_params.source_image
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_from_snapshot(self, snapshot):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_from_snapshot(
            PROJECT, INSTANCE_ZONE, instance_name, snapshot.self_link
        )
        try:
            assert (
                instance.disks[0].initialize_params.source_snapshot
                == snapshot.self_link
            )
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_with_additional_disk(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_additional_disk(PROJECT, INSTANCE_ZONE, instance_name)
        try:
            assert any(
                disk.initialize_params.disk_size_gb == 20 for disk in instance.disks
            )
            assert any(
                disk.initialize_params.disk_size_gb == 25 for disk in instance.disks
            )
            assert len(instance.disks) == 2
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_with_snapshotted_data_disk(self, snapshot):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_snapshotted_data_disk(
            PROJECT, INSTANCE_ZONE, instance_name, snapshot.self_link
        )
        try:
            assert any(
                disk.initialize_params.disk_size_gb == 11 for disk in instance.disks
            )
            assert any(
                disk.initialize_params.disk_size_gb == 10 for disk in instance.disks
            )
            assert len(instance.disks) == 2
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_with_subnet(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_subnet(
            PROJECT,
            INSTANCE_ZONE,
            instance_name,
            "global/networks/default",
            f"regions/{REGION}/subnetworks/default",
        )
        try:
            assert instance.network_interfaces[0].name == "global/networks/default"
            assert (
                instance.network_interfaces[0].subnetwork
                == f"regions/{REGION}/subnetworks/default"
            )
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
