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
import base64
import random
import string
import time
import uuid

import google.auth
from google.cloud import compute_v1
import pytest

from ..disks.clone_encrypted_disk import create_disk_from_customer_encrypted_disk
from ..disks.delete import delete_disk
from ..instances.change_machine_type import change_machine_type
from ..instances.get import get_instance
from ..instances.start import start_instance
from ..instances.start_encrypted import start_instance_with_encryption_key
from ..instances.stop import stop_instance

PROJECT = google.auth.default()[1]

INSTANCE_ZONE = "europe-west2-b"

KEY = "".join(random.sample(string.ascii_letters, 32))
KEY_B64 = base64.b64encode(
    KEY.encode()
)  # for example: b'VEdORldtY3NKellPdWRDcUF5YlNVREtJdm5qaFJYSFA='


def _make_disk(raw_key: bytes = None):
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-10"
    )
    initialize_params.disk_size_gb = 10
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True
    disk.type_ = "PERSISTENT"
    disk.device_name = "disk-1"

    if raw_key:
        disk.disk_encryption_key = compute_v1.CustomerEncryptionKey()
        disk.disk_encryption_key.raw_key = raw_key

    return disk


def _make_request(disk: compute_v1.AttachedDisk):
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "default"
    network_interface.access_configs = []

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.name = "i" + uuid.uuid4().hex[:10]
    instance.disks = [disk]
    full_machine_type_name = f"zones/{INSTANCE_ZONE}/machineTypes/e2-micro"
    instance.machine_type = full_machine_type_name
    instance.network_interfaces = [network_interface]

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = INSTANCE_ZONE
    request.project = PROJECT
    request.instance_resource = instance
    return request


def _create_instance(request: compute_v1.InsertInstanceRequest):
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    operation = instance_client.insert_unary(request=request)
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, zone=INSTANCE_ZONE, project=PROJECT
        )

    return instance_client.get(
        project=PROJECT, zone=INSTANCE_ZONE, instance=request.instance_resource.name
    )


def _delete_instance(instance: compute_v1.Instance):
    instance_client = compute_v1.InstancesClient()
    operation_client = compute_v1.ZoneOperationsClient()

    operation = instance_client.delete_unary(
        project=PROJECT, zone=INSTANCE_ZONE, instance=instance.name
    )
    while operation.status != compute_v1.Operation.Status.DONE:
        operation = operation_client.wait(
            operation=operation.name, zone=INSTANCE_ZONE, project=PROJECT
        )


def _get_status(instance: compute_v1.Instance) -> compute_v1.Instance.Status:
    instance_client = compute_v1.InstancesClient()
    return instance_client.get(
        project=PROJECT, zone=INSTANCE_ZONE, instance=instance.name
    ).status


@pytest.fixture
def compute_instance():
    disk = _make_disk()
    request = _make_request(disk)

    instance = _create_instance(request)

    yield instance

    _delete_instance(instance)


@pytest.fixture
def compute_encrypted_instance():
    disk = _make_disk(KEY_B64)
    request = _make_request(disk)

    instance = _create_instance(request)

    yield instance

    _delete_instance(instance)


@pytest.fixture
def autodelete_disk_name():
    name = "d" + uuid.uuid4().hex[:10]
    yield name
    delete_disk(PROJECT, INSTANCE_ZONE, name)


def test_instance_operations(compute_instance):
    assert _get_status(compute_instance) == "RUNNING"

    stop_instance(PROJECT, INSTANCE_ZONE, compute_instance.name)

    while _get_status(compute_instance) == "STOPPING":
        # Since we can't configure timeout parameter for operation wait() (b/188037306)
        # We need to do some manual waiting for the stopping to finish...
        time.sleep(5)

    assert _get_status(compute_instance) == "TERMINATED"

    start_instance(PROJECT, INSTANCE_ZONE, compute_instance.name)
    assert _get_status(compute_instance) == "RUNNING"


def test_instance_encrypted(compute_encrypted_instance):
    assert _get_status(compute_encrypted_instance) == "RUNNING"

    stop_instance(PROJECT, INSTANCE_ZONE, compute_encrypted_instance.name)
    while _get_status(compute_encrypted_instance) == "STOPPING":
        # Since we can't configure timeout parameter for operation wait() (b/188037306)
        # We need to do some manual waiting for the stopping to finish...
        time.sleep(5)

    assert _get_status(compute_encrypted_instance) == "TERMINATED"

    start_instance_with_encryption_key(
        PROJECT, INSTANCE_ZONE, compute_encrypted_instance.name, KEY_B64
    )
    assert _get_status(compute_encrypted_instance) == "RUNNING"


def test_clone_encrypted_disk(autodelete_disk_name, compute_encrypted_instance):
    assert _get_status(compute_encrypted_instance) == "RUNNING"

    new_disk = create_disk_from_customer_encrypted_disk(
        PROJECT, INSTANCE_ZONE, autodelete_disk_name,
        f"zones/{INSTANCE_ZONE}/diskTypes/pd-standard",
        10, compute_encrypted_instance.disks[0].source,
        encryption_key=KEY_B64)

    assert new_disk.name == autodelete_disk_name


def test_change_machine_type(compute_instance):
    assert _get_status(compute_instance) == "RUNNING"

    stop_instance(PROJECT, INSTANCE_ZONE, compute_instance.name)

    assert not get_instance(PROJECT, INSTANCE_ZONE, compute_instance.name).machine_type.endswith("e2-standard-2")
    change_machine_type(PROJECT, INSTANCE_ZONE, compute_instance.name, "e2-standard-2")

    assert get_instance(PROJECT, INSTANCE_ZONE, compute_instance.name).machine_type.endswith("e2-standard-2")
