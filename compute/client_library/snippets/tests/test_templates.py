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
import pytest

# Turning off F401 check because flake8 doesn't recognize using
# PyTest fixture as parameter as usage.
from .test_instance_start_stop import compute_instance  # noqa: F401

from ..instance_templates.create import create_template
from ..instance_templates.create_from_instance import \
    create_template_from_instance
from ..instance_templates.create_with_subnet import create_template_with_subnet
from ..instance_templates.delete import delete_instance_template
from ..instance_templates.list import list_instance_templates

PROJECT = google.auth.default()[1]

INSTANCE_ZONE = "europe-central2-b"


@pytest.fixture
def deletable_template_name():
    template_name = "i" + uuid.uuid4().hex[:10]
    yield template_name
    delete_instance_template(PROJECT, template_name)


@pytest.fixture
def template_to_be_deleted():
    template_name = "i" + uuid.uuid4().hex[:10]
    template = create_template(PROJECT, template_name)
    yield template


def test_create_template_and_list(deletable_template_name):

    template = create_template(PROJECT, deletable_template_name)

    assert template.name == deletable_template_name
    assert any(
        template.name == deletable_template_name
        for template in list_instance_templates(PROJECT)
    )
    assert template.properties.disks[0].initialize_params.disk_size_gb == 250
    assert "debian-11" in template.properties.disks[0].initialize_params.source_image
    assert template.properties.network_interfaces[0].name == "global/networks/default"
    assert template.properties.machine_type == "e2-standard-4"


def test_create_from_instance(compute_instance, deletable_template_name):  # noqa: F811

    template = create_template_from_instance(
        PROJECT, compute_instance.self_link, deletable_template_name
    )

    assert template.name == deletable_template_name
    assert template.properties.machine_type in compute_instance.machine_type
    assert (
        template.properties.disks[0].disk_size_gb
        == compute_instance.disks[0].disk_size_gb
    )
    assert (
        template.properties.disks[0].initialize_params.source_image
        == "projects/rocky-linux-cloud/global/images/family/rocky-linux-8"
    )


def test_create_template_with_subnet(deletable_template_name):
    template = create_template_with_subnet(
        PROJECT,
        "global/networks/default",
        "regions/asia-east1/subnetworks/default",
        deletable_template_name,
    )

    assert template.name == deletable_template_name
    assert (
        "global/networks/default" in template.properties.network_interfaces[0].network
    )
    assert (
        "regions/asia-east1/subnetworks/default"
        in template.properties.network_interfaces[0].subnetwork
    )


def test_delete_template(template_to_be_deleted):
    delete_instance_template(PROJECT, template_to_be_deleted.name)

    assert all(
        template.name != template_to_be_deleted.name
        for template in list_instance_templates(PROJECT)
    )
