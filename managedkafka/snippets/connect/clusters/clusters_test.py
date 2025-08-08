# Copyright 2025 Google LLC
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

from unittest import mock
from unittest.mock import MagicMock

from google.api_core.operation import Operation
from google.cloud import managedkafka_v1
import pytest

import create_connect_cluster  # noqa: I100
import delete_connect_cluster
import get_connect_cluster
import list_connect_clusters
import update_connect_cluster

PROJECT_ID = "test-project-id"
REGION = "us-central1"
KAFKA_CLUSTER_ID = "test-cluster-id"
CONNECT_CLUSTER_ID = "test-connect-cluster-id"


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connect_cluster"
)
def test_create_connect_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cpu = 12
    memory_bytes = 12884901900  # 12 GB
    primary_subnet = "test-subnet"
    operation = mock.MagicMock(spec=Operation)
    connect_cluster = managedkafka_v1.types.ConnectCluster()
    connect_cluster.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connect_cluster_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID
        )
    )
    operation.result = mock.MagicMock(return_value=connect_cluster)
    mock_method.return_value = operation

    create_connect_cluster.create_connect_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        kafka_cluster_id=KAFKA_CLUSTER_ID,
        primary_subnet=primary_subnet,
        cpu=cpu,
        memory_bytes=memory_bytes,
    )

    out, _ = capsys.readouterr()
    assert "Created Connect cluster" in out
    assert CONNECT_CLUSTER_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.get_connect_cluster"
)
def test_get_connect_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connect_cluster = managedkafka_v1.types.ConnectCluster()
    connect_cluster.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connect_cluster_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID
        )
    )
    mock_method.return_value = connect_cluster

    get_connect_cluster.get_connect_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got Connect cluster" in out
    assert CONNECT_CLUSTER_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.update_connect_cluster"
)
def test_update_connect_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    new_memory_bytes = 12884901900  # 12 GB
    operation = mock.MagicMock(spec=Operation)
    connect_cluster = managedkafka_v1.types.ConnectCluster()
    connect_cluster.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connect_cluster_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID
        )
    )
    connect_cluster.capacity_config.memory_bytes = new_memory_bytes
    operation.result = mock.MagicMock(return_value=connect_cluster)
    mock_method.return_value = operation

    update_connect_cluster.update_connect_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        memory_bytes=new_memory_bytes,
    )

    out, _ = capsys.readouterr()
    assert "Updated Connect cluster" in out
    assert CONNECT_CLUSTER_ID in out
    assert str(new_memory_bytes) in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.list_connect_clusters"
)
def test_list_connect_clusters(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connect_cluster = managedkafka_v1.types.ConnectCluster()
    connect_cluster.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connect_cluster_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID
        )
    )

    response = [connect_cluster]
    mock_method.return_value = response

    list_connect_clusters.list_connect_clusters(
        project_id=PROJECT_ID,
        region=REGION,
    )

    out, _ = capsys.readouterr()
    assert "Got Connect cluster" in out
    assert CONNECT_CLUSTER_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.delete_connect_cluster"
)
def test_delete_connect_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operation = mock.MagicMock(spec=Operation)
    mock_method.return_value = operation

    delete_connect_cluster.delete_connect_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Deleted Connect cluster" in out
    mock_method.assert_called_once()
