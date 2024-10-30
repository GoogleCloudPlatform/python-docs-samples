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
import uuid

from google.cloud.tpu_v2.types import AcceleratorConfig, Node

import pytest

import create_tpu
import create_tpu_topology
import create_tpu_with_script
import delete_tpu
import get_tpu
import list_tpu
import start_tpu
import stop_tpu


TPU_NAME = "test-tpu-" + uuid.uuid4().hex[:10]
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
ZONE = "us-south1-a"
TPU_TYPE = "v5litepod-1"
TPU_VERSION = "tpu-vm-tf-2.17.0-pjrt"


# Instance of TPU
@pytest.fixture(scope="session")
def tpu_instance() -> Node:
    yield create_tpu.create_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME, TPU_TYPE, TPU_VERSION)
    try:
        delete_tpu.delete_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    except Exception as e:
        print(f"Error during cleanup: {e}")


def test_creating_tpu(tpu_instance: Node) -> None:
    assert tpu_instance.state == Node.State.READY


def test_creating_with_startup_script() -> None:
    tpu_name_with_script = "script-tpu-" + uuid.uuid4().hex[:5]
    try:
        tpu_with_script = create_tpu_with_script.create_cloud_tpu_with_script(
            PROJECT_ID, ZONE, tpu_name_with_script, TPU_TYPE, TPU_VERSION
        )
        assert "--upgrade numpy" in tpu_with_script.metadata["startup-script"]
    finally:
        print(f"\n\n ------------ Deleting TPU {TPU_NAME}\n ------------")
        delete_tpu.delete_cloud_tpu(PROJECT_ID, ZONE, tpu_name_with_script)


def test_get_tpu() -> None:
    tpu = get_tpu.get_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    assert tpu.state == Node.State.READY
    assert tpu.name == f"projects/{PROJECT_ID}/locations/{ZONE}/nodes/{TPU_NAME}"


def test_list_tpu() -> None:
    nodes = list_tpu.list_cloud_tpu(PROJECT_ID, ZONE)
    assert len(list(nodes)) > 0


def test_stop_tpu() -> None:
    node = stop_tpu.stop_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    assert node.state == Node.State.STOPPED


def test_start_tpu() -> None:
    node = start_tpu.start_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    assert node.state == Node.State.READY


def test_with_topology() -> None:
    topology_tpu_name = "topology-tpu-" + uuid.uuid4().hex[:5]
    topology_zone = "us-central1-a"
    try:
        topology_tpu = create_tpu_topology.create_cloud_tpu_with_topology(
            PROJECT_ID, topology_zone, topology_tpu_name, TPU_VERSION
        )
        assert topology_tpu.accelerator_config.type_ == AcceleratorConfig.Type.V3
        assert topology_tpu.accelerator_config.topology == "2x2"
    finally:
        delete_tpu.delete_cloud_tpu(PROJECT_ID, topology_zone, topology_tpu_name)
