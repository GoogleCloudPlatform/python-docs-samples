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

from ..instances.bulk_insert import create_five_instances
from ..instances.delete import delete_instance

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "australia-southeast1-a"


@pytest.fixture
def instance_template():
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 25
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


def test_bulk_create(instance_template):
    name_pattern = "i-##-" + uuid.uuid4().hex[:5]

    instances = create_five_instances(PROJECT, INSTANCE_ZONE, instance_template.name,
                                      name_pattern)

    names = [instance.name for instance in instances]
    try:
        for i in range(1, 6):
            name = name_pattern.replace('##', f"0{i}")
            assert name in names
    finally:
        for name in names:
            delete_instance(PROJECT, INSTANCE_ZONE, name)
