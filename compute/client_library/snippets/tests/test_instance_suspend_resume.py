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
import time
import uuid

import google.auth
from google.cloud import compute_v1
import pytest


from ..images.get import get_image_from_family
from ..instances.create import create_instance, disk_from_image
from ..instances.delete import delete_instance
from ..instances.resume import resume_instance
from ..instances.suspend import suspend_instance

PROJECT = google.auth.default()[1]

INSTANCE_ZONE = "europe-west2-b"


def _get_status(instance: compute_v1.Instance) -> compute_v1.Instance.Status:
    instance_client = compute_v1.InstancesClient()
    return instance_client.get(
        project=PROJECT, zone=INSTANCE_ZONE, instance=instance.name
    ).status


@pytest.fixture
def compute_instance():
    instance_name = "test-instance-" + uuid.uuid4().hex[:10]
    newest_debian = get_image_from_family(project="ubuntu-os-cloud", family="ubuntu-2004-lts")
    disk_type = f"zones/{INSTANCE_ZONE}/diskTypes/pd-standard"
    disks = [disk_from_image(disk_type, 100, True, newest_debian.self_link)]
    instance = create_instance(
        PROJECT, INSTANCE_ZONE, instance_name, disks
    )
    yield instance

    delete_instance(PROJECT, INSTANCE_ZONE, instance_name)


def test_instance_suspend_resume(compute_instance):
    assert _get_status(compute_instance) == compute_v1.Instance.Status.RUNNING.name

    # Once the machine is running, give it some time to fully start all processes
    # before trying to suspend it
    time.sleep(45)

    suspend_instance(PROJECT, INSTANCE_ZONE, compute_instance.name)

    while _get_status(compute_instance) == compute_v1.Instance.Status.SUSPENDING.name:
        time.sleep(5)

    assert _get_status(compute_instance) == compute_v1.Instance.Status.SUSPENDED.name

    resume_instance(PROJECT, INSTANCE_ZONE, compute_instance.name)
    assert _get_status(compute_instance) == compute_v1.Instance.Status.RUNNING.name
