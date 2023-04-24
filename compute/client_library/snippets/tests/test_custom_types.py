#  Copyright 2021 Google LLC
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
import pytest

from ..images.get import get_image_from_family
from ..instances.create import create_instance
from ..instances.create_start_instance.create_from_public_image import disk_from_image
from ..instances.custom_machine_types.create_shared_with_helper import (
    create_custom_shared_core_instance,
)
from ..instances.custom_machine_types.create_with_helper import create_custom_instance
from ..instances.custom_machine_types.helper_class import CustomMachineType
from ..instances.custom_machine_types.update_memory import (
    add_extended_memory_to_instance,
)
from ..instances.delete import delete_instance

PROJECT = google.auth.default()[1]
REGION = "us-central1"
INSTANCE_ZONE = "us-central1-b"


@pytest.fixture
def auto_delete_instance_name():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]
    yield instance_name
    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


@pytest.fixture
def instance():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]

    newest_debian = get_image_from_family(project="debian-cloud", family="debian-10")
    disk_type = f"zones/{INSTANCE_ZONE}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link)]

    instance = create_instance(
        PROJECT, INSTANCE_ZONE, instance_name, disks, "n2-custom-8-10240"
    )
    yield instance
    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


def test_custom_instance_creation(auto_delete_instance_name):
    # Need to import CustomMachineType from this module, or the assertion will fail
    from ..instances.custom_machine_types.create_with_helper import CustomMachineType

    instance = create_custom_instance(
        PROJECT,
        INSTANCE_ZONE,
        auto_delete_instance_name,
        CustomMachineType.CPUSeries.E2,
        4,
        8192,
    )

    assert instance.name == auto_delete_instance_name
    assert instance.machine_type.endswith(
        f"zones/{INSTANCE_ZONE}/machineTypes/e2-custom-4-8192"
    )


def test_custom_shared_instance_creation(auto_delete_instance_name):
    # Need to import CustomMachineType from this module, or the assertion will fail
    from ..instances.custom_machine_types.create_shared_with_helper import (
        CustomMachineType,
    )

    instance = create_custom_shared_core_instance(
        PROJECT,
        INSTANCE_ZONE,
        auto_delete_instance_name,
        CustomMachineType.CPUSeries.E2_MICRO,
        2048,
    )

    assert instance.name == auto_delete_instance_name
    assert instance.machine_type.endswith(
        f"zones/{INSTANCE_ZONE}/machineTypes/e2-custom-micro-2048"
    )


def test_custom_machine_type_good():
    # N1
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.N1, 8192, 8)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/custom-8-8192"
    assert cmt.short_type_str() == "custom-8-8192"
    # N2
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.N2, 4096, 4)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/n2-custom-4-4096"
    assert cmt.short_type_str() == "n2-custom-4-4096"
    # N2D
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.N2D, 8192, 4)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/n2d-custom-4-8192"
    assert cmt.short_type_str() == "n2d-custom-4-8192"
    # E2
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.E2, 8192, 8)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/e2-custom-8-8192"
    assert cmt.short_type_str() == "e2-custom-8-8192"
    # E2 SMALL
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.E2_SMALL, 4096)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/e2-custom-small-4096"
    assert cmt.short_type_str() == "e2-custom-small-4096"
    # E2 MICRO
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.E2_MICRO, 2048)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/e2-custom-micro-2048"
    assert cmt.short_type_str() == "e2-custom-micro-2048"
    # E2 MEDIUM
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.E2_MEDIUM, 8192)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/e2-custom-medium-8192"
    assert cmt.short_type_str() == "e2-custom-medium-8192"


def test_custom_machine_type_bad_memory_256():
    try:
        CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.N1, 8194, 8)
    except RuntimeError as err:
        assert err.args[0] == "Requested memory must be a multiple of 256 MB."
    else:
        assert not "This test should have raised an exception!"


def test_custom_machine_type_ext_memory():
    cmt = CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.N2, 638720, 8)
    assert str(cmt) == f"zones/{INSTANCE_ZONE}/machineTypes/n2-custom-8-638720-ext"


def test_custom_machine_type_bad_cpu_count():
    try:
        CustomMachineType(INSTANCE_ZONE, CustomMachineType.CPUSeries.N2, 8194, 66)
    except RuntimeError as err:
        assert err.args[0].startswith(
            "Invalid number of cores requested. Allowed number of cores for"
        )
    else:
        assert not "This test should have raised an exception!"


def test_add_extended_memory_to_instance(instance):
    instance = add_extended_memory_to_instance(
        PROJECT, INSTANCE_ZONE, instance.name, 819200
    )
    assert instance.machine_type.endswith("819200-ext")


def test_from_str_creation():
    cmt = CustomMachineType.from_str(
        "https://www.googleapis.com/compute/v1/projects/diregapic-mestiv/zones/us-central1-b/machineTypes/e2-custom-4-8192"
    )
    assert cmt.zone == "us-central1-b"
    assert cmt.memory_mb == 8192
    assert cmt.extra_memory_used is False
    assert cmt.cpu_series is CustomMachineType.CPUSeries.E2
    assert cmt.core_count == 4

    cmt = CustomMachineType.from_str(
        "zones/europe-west4-b/machineTypes/n2-custom-8-81920-ext"
    )
    assert cmt.zone == "europe-west4-b"
    assert cmt.memory_mb == 81920
    assert cmt.extra_memory_used is True
    assert cmt.cpu_series is CustomMachineType.CPUSeries.N2
    assert cmt.core_count == 8

    cmt = CustomMachineType.from_str(
        "zones/europe-west4-b/machineTypes/e2-custom-small-4096"
    )
    assert cmt.zone == "europe-west4-b"
    assert cmt.memory_mb == 4096
    assert cmt.extra_memory_used is False
    assert cmt.cpu_series == CustomMachineType.CPUSeries.E2_SMALL
    assert cmt.core_count == 2

    cmt = CustomMachineType.from_str(
        "zones/europe-west2-b/machineTypes/custom-2-2048"
    )
    assert cmt.zone == "europe-west2-b"
    assert cmt.memory_mb == 2048
    assert cmt.extra_memory_used is False
    assert cmt.cpu_series is CustomMachineType.CPUSeries.N1
    assert cmt.core_count == 2

    try:
        CustomMachineType.from_str(
            "zones/europe-west2-b/machineTypes/n8-custom-2-1024"
        )
    except RuntimeError as err:
        assert err.args[0] == "Unknown CPU series."
    else:
        assert not "This was supposed to raise a RuntimeError."

    cmt = CustomMachineType.from_str("n2d-custom-8-81920-ext")
    assert cmt.zone is None
    assert cmt.memory_mb == 81920
    assert cmt.extra_memory_used is True
    assert cmt.cpu_series is CustomMachineType.CPUSeries.N2D
    assert cmt.core_count == 8
