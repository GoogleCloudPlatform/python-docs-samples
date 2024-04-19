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

from ..instances.create_start_instance.create_from_public_image import (
    create_from_public_image,
    create_instance,
    disk_from_image,
    get_image_from_family,
)

from ..instances.delete import delete_instance
from ..instances.ip_address.get_vm_address import get_instance_ip_address, IPType


PROJECT = google.auth.default()[1]
REGION = "us-central1"
INSTANCE_ZONE = "us-central1-b"


def test_get_instance_internal_ip_address():
    instance_name = "i" + uuid.uuid4().hex[:10]
    instance = create_from_public_image(
        PROJECT,
        INSTANCE_ZONE,
        instance_name,
    )
    try:
        internal_ip = get_instance_ip_address(instance, IPType.INTERNAL)
        assert internal_ip == instance.network_interfaces[0].network_i_p
    finally:
        delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


def test_get_instance_external_ip_address():
    instance_name = "i" + uuid.uuid4().hex[:10]
    newest_debian = get_image_from_family(project="debian-cloud", family="debian-10")
    disk_type = f"zones/{INSTANCE_ZONE}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 10, True, newest_debian.self_link, True)]
    instance = create_instance(
        PROJECT, INSTANCE_ZONE, instance_name, disks, external_access=True
    )
    try:
        external_ip = get_instance_ip_address(instance, IPType.EXTERNAL)
        assert external_ip == instance.network_interfaces[0].access_configs[0].nat_i_p
    finally:
        delete_instance(PROJECT, INSTANCE_ZONE, instance_name)
