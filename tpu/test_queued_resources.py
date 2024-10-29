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
from typing import Callable

import uuid

from google.cloud.tpu_v2alpha1 import QueuedResource

import pytest

import queued_resources_create
import queued_resources_create_network
import queued_resources_create_startup_script
import queued_resources_create_time_bound
import queued_resources_delete_force
import queued_resources_list


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
ZONE = "us-central1-b"
TPU_TYPE = "v2-8"
TPU_VERSION = "tpu-vm-tf-2.17.0-pjrt"


@pytest.fixture(scope="function")
def test_resource_name() -> None:
    yield "test-resource-" + uuid.uuid4().hex[:6]


@pytest.fixture(scope="function")
def test_tpu_name() -> None:
    yield "test-tpu-" + uuid.uuid4().hex[:6]


@pytest.fixture(scope="function")
def create_resource() -> Callable:
    resources = []

    def _create_resource(
        create_func: Callable, resource_name: str, tpu_name: str
    ) -> QueuedResource:
        resource = create_func(
            PROJECT_ID,
            ZONE,
            tpu_name,
            TPU_TYPE,
            TPU_VERSION,
            resource_name,
        )
        resources.append((resource_name, tpu_name))
        assert resource_name in resource.name
        return resource

    yield _create_resource
    for resource_name, tpu_name in resources:
        queued_resources_delete_force.delete_force_queued_resource(
            PROJECT_ID, ZONE, resource_name
        )


def test_list_queued_resources(
    create_resource: Callable, test_resource_name: str, test_tpu_name: str
) -> None:
    create_resource(
        queued_resources_create.create_queued_resource,
        test_resource_name,
        test_tpu_name,
    )
    resources = queued_resources_list.list_queued_resources(PROJECT_ID, ZONE)
    assert any(
        test_resource_name in resource.name for resource in resources
    ), f"Resources does not contain '{test_resource_name}'"


def test_create_resource_with_network(
    create_resource: Callable, test_resource_name: str, test_tpu_name: str
) -> None:
    resource = create_resource(
        queued_resources_create_network.create_queued_resource_network,
        test_resource_name,
        test_tpu_name,
    )
    assert resource.tpu.node_spec[0].node.network_config.network == "default"


def test_create_resource_with_startup_script(
    create_resource: Callable, test_resource_name: str, test_tpu_name: str
) -> None:
    resource = create_resource(
        queued_resources_create_startup_script.create_queued_resource_startup_script,
        test_resource_name,
        test_tpu_name,
    )
    assert (
        "--upgrade numpy" in resource.tpu.node_spec[0].node.metadata["startup-script"]
    )


def test_create_queued_resource_time_bound(
    create_resource: Callable, test_resource_name: str, test_tpu_name: str
) -> None:
    resource = create_resource(
        queued_resources_create_time_bound.create_queued_resource_time_bound,
        test_resource_name,
        test_tpu_name,
    )
    assert resource.queueing_policy.valid_until_time
