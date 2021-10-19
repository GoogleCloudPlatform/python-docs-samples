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


from quickstart import delete_instance, wait_for_operation
from sample_create_vm import (
    create_from_custom_image,
    create_from_public_image,
    create_from_snapshot,
    create_with_additional_disk,
    create_with_snapshotted_data_disk,
    create_with_subnet,
)

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "europe-central2-b"


def get_active_debian():
    image_client = compute_v1.ImagesClient()

    return image_client.get_from_family(project="debian-cloud", family="debian-11")


@pytest.fixture(scope="class")
def src_disk(request):
    disk_client = compute_v1.DisksClient()

    disk = compute_v1.Disk()
    disk.source_image = get_active_debian().self_link
    disk.name = "test-disk-" + uuid.uuid4().hex[:10]
    op = disk_client.insert(project=PROJECT, zone=INSTANCE_ZONE, disk_resource=disk)

    wait_for_operation(op, PROJECT)
    disk = disk_client.get(project=PROJECT, zone=INSTANCE_ZONE, disk=disk.name)
    request.cls.disk = disk

    yield disk

    op = disk_client.delete(project=PROJECT, zone=INSTANCE_ZONE, disk=disk.name)
    wait_for_operation(op, PROJECT)


@pytest.fixture(scope="class")
def snapshot(request, src_disk):
    snapshot_client = compute_v1.SnapshotsClient()
    snapshot = compute_v1.Snapshot()
    snapshot.name = "test-snap-" + uuid.uuid4().hex[:10]
    disk_client = compute_v1.DisksClient()
    op = disk_client.create_snapshot(
        project=PROJECT,
        zone=INSTANCE_ZONE,
        disk=src_disk.name,
        snapshot_resource=snapshot,
    )
    wait_for_operation(op, PROJECT)

    request.cls.snapshot = snapshot_client.get(project=PROJECT, snapshot=snapshot.name)
    snapshot = request.cls.snapshot

    yield snapshot

    op = snapshot_client.delete(project=PROJECT, snapshot=snapshot.name)
    wait_for_operation(op, PROJECT)


@pytest.fixture(scope="class")
def image(request, src_disk):
    image_client = compute_v1.ImagesClient()
    image = compute_v1.Image()
    image.source_disk = src_disk.self_link
    image.name = "test-image-" + uuid.uuid4().hex[:10]
    op = image_client.insert(project=PROJECT, image_resource=image)

    wait_for_operation(op, PROJECT)

    image = image_client.get(project=PROJECT, image=image.name)
    request.cls.image = image
    yield image

    op = image_client.delete(project=PROJECT, image=image.name)
    wait_for_operation(op, PROJECT)


@pytest.fixture()
def subnetwork():
    network_client = compute_v1.NetworksClient()
    network = compute_v1.Network()
    network.name = "test-network-" + uuid.uuid4().hex[:10]
    network.auto_create_subnetworks = True
    op = network_client.insert(project=PROJECT, network_resource=network)
    wait_for_operation(op, PROJECT)
    network = network_client.get(project=PROJECT, network=network.name)

    subnet = compute_v1.Subnetwork()
    subnet.name = "test-subnet-" + uuid.uuid4().hex[:10]
    subnet.network = network_client.get(project=PROJECT, network=network.name).self_link
    subnet.region = "europe-central2"
    subnet.ip_cidr_range = "10.0.0.0/20"
    subnet_client = compute_v1.SubnetworksClient()
    op = subnet_client.insert(
        project=PROJECT, region="europe-central2", subnetwork_resource=subnet
    )
    wait_for_operation(op, PROJECT)
    subnet = subnet_client.get(
        project=PROJECT, region="europe-central2", subnetwork=subnet.name
    )

    yield subnet

    op = subnet_client.delete(project=PROJECT, region='europe-central2', subnetwork=subnet.name)
    wait_for_operation(op, PROJECT)

    op = network_client.delete(project=PROJECT, network=network.name)
    wait_for_operation(op, PROJECT)


@pytest.mark.usefixtures("image", "snapshot")
class TestCreation:
    def test_create_from_custom_image(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_from_custom_image(
            PROJECT, INSTANCE_ZONE, instance_name, self.image.self_link
        )
        try:
            assert (
                instance.disks[0].initialize_params.source_image == self.image.self_link
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

    def test_create_from_snapshot(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_from_snapshot(
            PROJECT, INSTANCE_ZONE, instance_name, self.snapshot.self_link
        )
        try:
            assert (
                instance.disks[0].initialize_params.source_snapshot
                == self.snapshot.self_link
            )
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)

    def test_create_with_additional_disk(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_additional_disk(PROJECT, INSTANCE_ZONE, instance_name)
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

    def test_create_with_snapshotted_data_disk(self):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_snapshotted_data_disk(
            PROJECT, INSTANCE_ZONE, instance_name, self.snapshot.self_link
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

    def test_create_with_subnet(self, subnetwork):
        instance_name = "i" + uuid.uuid4().hex[:10]
        instance = create_with_subnet(
            PROJECT,
            INSTANCE_ZONE,
            instance_name,
            subnetwork.network,
            subnetwork.self_link,
        )
        try:
            assert instance.network_interfaces[0].name == subnetwork.network
            assert instance.network_interfaces[0].subnetwork == subnetwork.self_link
        finally:
            delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
