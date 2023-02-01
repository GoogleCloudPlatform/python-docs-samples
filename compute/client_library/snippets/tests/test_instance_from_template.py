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
from google.cloud import compute_v1
import pytest

from ..instances.delete import delete_instance
from ..instances.from_instance_template.create_from_template import (
    create_instance_from_template,
)
from ..instances.from_instance_template.create_from_template_with_overrides import (
    create_instance_from_template_with_overrides,
)

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "europe-north1-c"


@pytest.fixture
def instance_template():
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 25
    initialize_params.disk_type = 'pd-balanced'
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"

    template = compute_v1.InstanceTemplate()
    template.name = "test-template-" + uuid.uuid4().hex[:10]
    template.properties.disks = [disk]
    template.properties.machine_type = "n1-standard-4"
    template.properties.network_interfaces = [network_interface]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert_unary(
        project=PROJECT, instance_template_resource=template
    )
    operation_client.wait(project=PROJECT, operation=op.name)

    template = template_client.get(project=PROJECT, instance_template=template.name)

    yield template

    op = template_client.delete_unary(project=PROJECT, instance_template=template.name)
    operation_client.wait(project=PROJECT, operation=op.name)


@pytest.fixture()
def autodelete_instance_name():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]
    yield instance_name
    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


def test_create_instance_from_template(instance_template, autodelete_instance_name):
    instance = create_instance_from_template(
        PROJECT, INSTANCE_ZONE, autodelete_instance_name, instance_template.self_link
    )

    assert instance.name == autodelete_instance_name
    assert instance.zone.endswith(INSTANCE_ZONE)


def test_create_instance_from_template_override(
    instance_template, autodelete_instance_name
):
    image_client = compute_v1.ImagesClient()

    image = image_client.get_from_family(
        project="ubuntu-os-cloud", family="ubuntu-2004-lts"
    )
    instance = create_instance_from_template_with_overrides(
        PROJECT,
        INSTANCE_ZONE,
        autodelete_instance_name,
        instance_template.name,
        f"zones/{INSTANCE_ZONE}/machineTypes/n2-standard-2",
        image.self_link,
    )

    assert instance.name == autodelete_instance_name
    assert instance.machine_type.endswith("n2-standard-2")
    assert len(instance.disks) == 2
