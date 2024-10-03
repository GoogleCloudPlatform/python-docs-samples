#  Copyright 2024 Google LLC
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

from ..instance_templates.create_reservation_from_template import (
    create_reservation_from_template,
)

PROJECT = google.auth.default()[1]
INSTANCE_ZONE = "us-central1-a"


@pytest.fixture
def instance_template():
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/debian-cloud/global/images/family/debian-11"
    )
    initialize_params.disk_size_gb = 25
    initialize_params.disk_type = "pd-balanced"
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
def autodelete_reservation_name():
    instance_name = "test-reservation-" + uuid.uuid4().hex[:10]
    yield instance_name
    reservations_client = compute_v1.ReservationsClient()
    reservations_client.delete(
        project=PROJECT, zone=INSTANCE_ZONE, reservation=instance_name
    )


def test_create_reservation_from_template(
    instance_template, autodelete_reservation_name
):
    reservation = create_reservation_from_template(
        PROJECT, autodelete_reservation_name, instance_template.self_link
    )

    assert reservation.name == autodelete_reservation_name
    assert reservation.zone.endswith(INSTANCE_ZONE)
    assert (
        reservation.specific_reservation.source_instance_template
        == instance_template.self_link
    )
