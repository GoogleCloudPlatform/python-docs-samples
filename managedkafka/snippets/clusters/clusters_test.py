# Copyright 2024 Google LLC
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

import create_cluster
import delete_cluster
import get_cluster
from google.api_core.operation import Operation
from google.cloud import managedkafka_v1
import list_clusters
import pytest
import update_cluster

PROJECT_ID = "test-project-id"
REGION = "us-central1"
CLUSTER_ID = "test-cluster-id"


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.create_cluster")
def test_create_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    cpu = 3
    memory_bytes = 3221225472
    subnet = "test-subnet"
    operation = mock.MagicMock(spec=Operation)
    cluster = managedkafka_v1.Cluster()
    cluster.name = managedkafka_v1.ManagedKafkaClient.cluster_path(
        PROJECT_ID, REGION, CLUSTER_ID
    )
    operation.result = mock.MagicMock(return_value=cluster)
    mock_method.return_value = operation

    create_cluster.create_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        subnet=subnet,
        cpu=cpu,
        memory_bytes=memory_bytes,
    )

    out, _ = capsys.readouterr()
    assert "Created cluster" in out
    assert CLUSTER_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.get_cluster")
def test_get_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    cluster = managedkafka_v1.Cluster()
    cluster.name = managedkafka_v1.ManagedKafkaClient.cluster_path(
        PROJECT_ID, REGION, CLUSTER_ID
    )
    mock_method.return_value = cluster

    get_cluster.get_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got cluster" in out
    assert CLUSTER_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.update_cluster")
def test_update_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    new_memory_bytes = 3221225475
    operation = mock.MagicMock(spec=Operation)
    cluster = managedkafka_v1.Cluster()
    cluster.name = managedkafka_v1.ManagedKafkaClient.cluster_path(
        PROJECT_ID, REGION, CLUSTER_ID
    )
    cluster.capacity_config.memory_bytes = new_memory_bytes
    operation.result = mock.MagicMock(return_value=cluster)
    mock_method.return_value = operation

    update_cluster.update_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
        memory_bytes=new_memory_bytes,
    )

    out, _ = capsys.readouterr()
    assert "Updated cluster" in out
    assert CLUSTER_ID in out
    assert str(new_memory_bytes) in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.list_clusters")
def test_list_clusters(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    cluster = managedkafka_v1.Cluster()
    cluster.name = managedkafka_v1.ManagedKafkaClient.cluster_path(
        PROJECT_ID, REGION, CLUSTER_ID
    )
    response = [cluster]
    mock_method.return_value = response

    list_clusters.list_clusters(
        project_id=PROJECT_ID,
        region=REGION,
    )

    out, _ = capsys.readouterr()
    assert "Got cluster" in out
    assert CLUSTER_ID in out
    mock_method.assert_called_once()


@mock.patch("google.cloud.managedkafka_v1.ManagedKafkaClient.delete_cluster")
def test_delete_cluster(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
):
    operation = mock.MagicMock(spec=Operation)
    mock_method.return_value = operation

    delete_cluster.delete_cluster(
        project_id=PROJECT_ID,
        region=REGION,
        cluster_id=CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Deleted cluster" in out
    mock_method.assert_called_once()
