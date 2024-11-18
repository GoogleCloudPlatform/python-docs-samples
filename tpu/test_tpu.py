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
from unittest.mock import MagicMock, patch

import uuid

from google.cloud.tpu_v2.services.tpu.pagers import ListNodesPager
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


TPU_NAME = "test-tpu-" + uuid.uuid4().hex[:6]
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
ZONE = "us-south1-a"
FULL_TPU_NAME = f"projects/{PROJECT_ID}/locations/{ZONE}/nodes/{TPU_NAME}"
TPU_TYPE = "v5litepod-1"
TPU_VERSION = "tpu-vm-tf-2.17.0-pjrt"
METADATA = {
    "startup-script": """#!/bin/bash
    echo "Hello World" > /var/log/hello.log
    sudo pip3 install --upgrade numpy >> /var/log/hello.log 2>&1
    """
}


@pytest.fixture
def mock_tpu_client() -> MagicMock:
    with patch("google.cloud.tpu_v2.TpuClient") as mock_client:
        yield mock_client.return_value


@pytest.fixture
def operation() -> MagicMock:
    yield MagicMock()


def test_creating_tpu(mock_tpu_client: MagicMock, operation: MagicMock) -> None:
    mock_response = MagicMock(spec=Node)
    mock_response.state = Node.State.READY
    mock_response.name = FULL_TPU_NAME

    mock_tpu_client.create_node.return_value = operation
    operation.result.return_value = mock_response

    tpu = create_tpu.create_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME, TPU_TYPE, TPU_VERSION)

    assert tpu.name == FULL_TPU_NAME
    assert tpu.state == Node.State.READY
    mock_tpu_client.create_node.assert_called_once()
    operation.result.assert_called_once()


def test_delete_tpu(mock_tpu_client: MagicMock) -> None:
    delete_tpu.delete_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)
    mock_tpu_client.delete_node.assert_called_once()


def test_creating_with_startup_script(
    mock_tpu_client: MagicMock, operation: MagicMock
) -> None:
    mock_response = MagicMock(spec=Node)
    mock_response.metadata = METADATA
    mock_tpu_client.create_node.return_value = operation
    operation.result.return_value = mock_response

    tpu_with_script = create_tpu_with_script.create_cloud_tpu_with_script(
        PROJECT_ID, ZONE, TPU_NAME, TPU_TYPE, TPU_VERSION
    )

    mock_tpu_client.create_node.assert_called_once()
    operation.result.assert_called_once()
    assert "--upgrade numpy" in tpu_with_script.metadata["startup-script"]


def test_get_tpu(mock_tpu_client: MagicMock) -> None:
    mock_response = MagicMock(spec=Node)
    mock_response.name = FULL_TPU_NAME
    mock_response.state = Node.State.READY

    mock_tpu_client.get_node.return_value = mock_response

    tpu = get_tpu.get_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)

    assert tpu.state == Node.State.READY
    assert tpu.name == FULL_TPU_NAME
    mock_tpu_client.get_node.assert_called_once()


def test_list_tpu(mock_tpu_client: MagicMock) -> None:
    mock_pager = MagicMock(spec=ListNodesPager)
    nodes = [
        Node(name="Node1", state=Node.State.READY),
        Node(name="Node2", state=Node.State.CREATING),
    ]
    mock_pager.__iter__.return_value = nodes

    mock_tpu_client.list_nodes.return_value = mock_pager

    nodes = list_tpu.list_cloud_tpu(PROJECT_ID, ZONE)
    assert len(list(nodes)) > 0
    mock_tpu_client.list_nodes.assert_called_once()


def test_stop_tpu(mock_tpu_client: MagicMock, operation: MagicMock) -> None:
    mock_response = MagicMock(spec=Node)
    mock_response.state = Node.State.STOPPED

    mock_tpu_client.stop_node.return_value = operation
    operation.result.return_value = mock_response

    node = stop_tpu.stop_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)

    mock_tpu_client.stop_node.assert_called_once()
    operation.result.assert_called_once()
    assert node.state == Node.State.STOPPED


def test_start_tpu(mock_tpu_client: MagicMock, operation: MagicMock) -> None:
    mock_response = MagicMock(spec=Node)
    mock_response.state = Node.State.READY

    mock_tpu_client.start_node.return_value = operation
    operation.result.return_value = mock_response

    node = start_tpu.start_cloud_tpu(PROJECT_ID, ZONE, TPU_NAME)

    mock_tpu_client.start_node.assert_called_once()
    operation.result.assert_called_once()
    assert node.state == Node.State.READY


def test_with_topology(mock_tpu_client: MagicMock, operation: MagicMock) -> None:
    from google.cloud import tpu_v2

    mock_response = MagicMock(spec=Node)
    mock_response.accelerator_config = tpu_v2.AcceleratorConfig(
        type_=tpu_v2.AcceleratorConfig.Type.V3,
        topology="2x2",
    )

    mock_tpu_client.create_node.return_value = operation
    operation.result.return_value = mock_response

    topology_tpu = create_tpu_topology.create_cloud_tpu_with_topology(
        PROJECT_ID, ZONE, TPU_NAME, TPU_VERSION
    )
    assert topology_tpu.accelerator_config.type_ == AcceleratorConfig.Type.V3
    assert topology_tpu.accelerator_config.topology == "2x2"
    mock_tpu_client.create_node.assert_called_once()
    operation.result.assert_called_once()
