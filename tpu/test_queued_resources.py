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

from google.cloud.tpu_v2 import Node
from google.cloud.tpu_v2alpha1 import QueuedResourceState as States

import pytest

import delete_tpu
import get_tpu
import queued_resources_create
import queued_resources_delete
import queued_resources_get
import queued_resources_list

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
ZONE = "us-central1-b"
TPU_TYPE = "v2-8"
TPU_VERSION = "tpu-vm-tf-2.17.0-pjrt"

STATUSES = [
    States.State.ACCEPTED,
    States.State.WAITING_FOR_RESOURCES,
    States.State.SUSPENDED,
    States.State.FAILED,
]


@pytest.fixture(scope="function")
def test_resource_name() -> None:
    yield "test-resource-" + uuid.uuid4().hex[:6]


@pytest.fixture(scope="function")
def test_tpu_name() -> None:
    yield "test-tpu-" + uuid.uuid4().hex[:6]


# Here we need to make sure that we have not left the working TPU.
# The test is made so that if resources manage to create TPU before their
# actual removal we wait until TPU is created, delete it and wait for changing
# the status of queued_resources until one that will allow us to delete it
def clean_resource(resource_name: str, tpu_name: str) -> None:
    while True:
        resource = queued_resources_get.get_queued_resources(
            PROJECT_ID, ZONE, resource_name
        )
        if resource.state.state in STATUSES:
            try:
                print(f"Attempting to delete resource '{resource_name}'...")
                queued_resources_delete.delete_queued_resources(
                    PROJECT_ID, ZONE, resource_name
                )
                print("Resource and TPU successfully deleted. Exiting...")
                return True
            except Exception:
                print("Resource is not in a deletable state. Waiting...")
                continue
        time.sleep(60)
        try:
            print(f"Attempting to delete TPU '{tpu_name}'...")
            node = get_tpu.get_cloud_tpu(PROJECT_ID, ZONE, tpu_name)
            if node and node.state == Node.State.READY:
                delete_tpu.delete_cloud_tpu(PROJECT_ID, ZONE, tpu_name)
        except Exception:
            print("TPU is not ready for deletion. Waiting...")
            continue


def test_create_resource(test_resource_name: str, test_tpu_name: str) -> None:
    try:
        resource = queued_resources_create.create_queued_resources(
            PROJECT_ID, ZONE, test_tpu_name, TPU_TYPE, TPU_VERSION, test_resource_name
        )
        assert test_resource_name in resource.name
    finally:
        assert clean_resource(test_resource_name, test_tpu_name)


def test_list_queued_resources(test_resource_name: str, test_tpu_name: str) -> None:
    try:
        queued_resources_create.create_queued_resources(
            PROJECT_ID, ZONE, test_tpu_name, TPU_TYPE, TPU_VERSION, test_resource_name
        )
        resources = queued_resources_list.list_queued_resources(PROJECT_ID, ZONE)
        assert any(
            test_resource_name in resource.name for resource in resources
        ), f"Resources does not contain '{test_resource_name}'"
    finally:
        assert clean_resource(test_resource_name, test_tpu_name)
