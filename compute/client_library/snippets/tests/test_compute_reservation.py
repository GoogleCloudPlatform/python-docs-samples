# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import time
import uuid

from google.cloud import compute_v1
from google.cloud.compute_v1.types import Operation

import pytest

from ..compute_reservations.create_compute_reservation import create_compute_reservation
from ..compute_reservations.create_compute_reservation_from_vm import (
    create_compute_reservation_from_vm,
)
from ..compute_reservations.delete_compute_reservation import delete_compute_reservation
from ..compute_reservations.get_compute_reservation import get_compute_reservation
from ..compute_reservations.list_compute_reservation import list_compute_reservation


from ..instances.create import create_instance
from ..instances.delete import delete_instance

INSTANCE_NAME = "test-instance-" + uuid.uuid4().hex[:10]
RESERVATION_NAME = "test-reservation-" + uuid.uuid4().hex[:10]
TIMEOUT = time.time() + 300  # 5 minutes
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
ZONE = "us-central1-a"
MACHINE_TYPE = "n2-standard-2"


@pytest.fixture()
def reservation(request) -> str:
    create_compute_reservation(PROJECT_ID, ZONE, RESERVATION_NAME)

    def cleanup():
        try:
            delete_compute_reservation(PROJECT_ID, ZONE, RESERVATION_NAME)
        except Exception as e:
            print(f"Error during cleanup: {e}")

    request.addfinalizer(cleanup)

    reservation = get_compute_reservation(PROJECT_ID, ZONE, RESERVATION_NAME)
    return reservation


@pytest.fixture(scope="session")
def vm_instance():
    """the fixture should create a VM instance"""
    boot_disk = compute_v1.AttachedDisk()
    boot_disk.auto_delete = True
    boot_disk.boot = True
    boot_disk.initialize_params = compute_v1.AttachedDiskInitializeParams(
        source_image="projects/debian-cloud/global/images/family/debian-11"
    )

    additional_disk = compute_v1.AttachedDisk()
    additional_disk.auto_delete = True
    additional_disk.boot = False
    additional_disk.initialize_params = compute_v1.AttachedDiskInitializeParams(
        disk_size_gb=375
    )
    additional_disk.interface = "SCSI"

    instance = create_instance(
        project_id=PROJECT_ID,
        zone=ZONE,
        instance_name=INSTANCE_NAME,
        disks=[boot_disk, additional_disk],
        machine_type=MACHINE_TYPE,
    )
    yield instance

    try:
        delete_instance(PROJECT_ID, ZONE, INSTANCE_NAME)
    except Exception as e:
        print(f"Error during cleanup: {e}")

    return instance


def test_create_compute_reservation_from_vm(vm_instance):
    try:
        res_from_vm = create_compute_reservation_from_vm(
            PROJECT_ID, ZONE, RESERVATION_NAME, vm_instance.name
        )
        assert res_from_vm.status == "READY"
        assert (
            res_from_vm.specific_reservation.instance_properties.local_ssds[
                0
            ].disk_size_gb
            == vm_instance.disks[1].disk_size_gb
        )
        assert (
            res_from_vm.specific_reservation.instance_properties.local_ssds[0].interface
            == vm_instance.disks[1].interface
        )
    finally:
        delete_compute_reservation(PROJECT_ID, ZONE, RESERVATION_NAME)


def test_create_and_get_compute_reservation(reservation):
    assert reservation.name == RESERVATION_NAME
    assert reservation.status == "READY"


def test_list_compute_reservation(reservation):
    response = list_compute_reservation(PROJECT_ID, ZONE)
    for reservation in response:
        if reservation.name == RESERVATION_NAME:
            assert True
            return
    assert False, f"Reservation {RESERVATION_NAME} not found in the list"


def test_delete_compute_reservation(reservation):
    response = delete_compute_reservation(PROJECT_ID, ZONE, reservation.name)
    assert response.status == Operation.Status.DONE
