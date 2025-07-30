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

import create_bigquery_sink_connector
import create_mirrormaker_connector
import create_pubsub_sink_connector
import create_pubsub_source_connector
import create_storage_sink_connector
import delete_connector
import get_connector
import list_connectors
import pause_connector
import restart_connector
import resume_connector
import stop_connector
import update_connector

PROJECT_ID = "test-project-id"
REGION = "us-central1"
CONNECT_CLUSTER_ID = "test-connect-cluster-id"
CONNECTOR_ID = "test-connector-id"
KAFKA_TOPIC = "test-topic"


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_mirrormaker_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "test-mirrormaker"
    source_cluster_dns = "source-cluster.example.com:9092"
    target_cluster_dns = "target-cluster.example.com:9092"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, connector_id
        )
    )
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_mirrormaker_connector.create_mirrormaker_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=connector_id,
        source_cluster_dns=source_cluster_dns,
        target_cluster_dns=target_cluster_dns,
        topic_name=KAFKA_TOPIC,
    )

    out, _ = capsys.readouterr()
    assert "Created MirrorMaker connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_pubsub_source_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "test-pubsub-source"
    subscription_id = "test-subscription"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, connector_id
        )
    )
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_pubsub_source_connector.create_pubsub_source_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=connector_id,
        kafka_topic=KAFKA_TOPIC,
        subscription_id=subscription_id,
    )

    out, _ = capsys.readouterr()
    assert "Created Pub/Sub source connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_pubsub_sink_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "test-pubsub-sink"
    pubsub_topic_id = "test-pubsub-topic"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, connector_id
        )
    )
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_pubsub_sink_connector.create_pubsub_sink_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=connector_id,
        kafka_topic=KAFKA_TOPIC,
        pubsub_topic_id=pubsub_topic_id,
    )

    out, _ = capsys.readouterr()
    assert "Created Pub/Sub sink connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_storage_sink_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "test-gcs-sink"
    bucket_name = "test-bucket"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, connector_id
        )
    )
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_storage_sink_connector.create_storage_sink_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=connector_id,
        kafka_topic=KAFKA_TOPIC,
        bucket_name=bucket_name,
    )

    out, _ = capsys.readouterr()
    assert "Created Cloud Storage sink connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_bigquery_sink_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "test-bq-sink"
    dataset_id = "test_dataset"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, connector_id
        )
    )
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_bigquery_sink_connector.create_bigquery_sink_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=connector_id,
        kafka_topic=KAFKA_TOPIC,
        dataset_id=dataset_id,
    )

    out, _ = capsys.readouterr()
    assert "Created BigQuery sink connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.list_connectors"
)
def test_list_connectors(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, CONNECTOR_ID
        )
    )
    mock_method.return_value = [connector]

    list_connectors.list_connectors(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.get_connector"
)
def test_get_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, CONNECTOR_ID
        )
    )
    mock_method.return_value = connector

    get_connector.get_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
    )

    out, _ = capsys.readouterr()
    assert "Got connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.update_connector"
)
def test_update_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    configs = {
        "tasks.max": "2",
        "value.converter.schemas.enable" : "true"
    }
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = (
        managedkafka_v1.ManagedKafkaConnectClient.connector_path(
            PROJECT_ID, REGION, CONNECT_CLUSTER_ID, CONNECTOR_ID
        )
    )
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    update_connector.update_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
        configs=configs,
    )

    out, _ = capsys.readouterr()
    assert "Updated connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.delete_connector"
)
def test_delete_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operation = mock.MagicMock(spec=Operation)
    operation.result = mock.MagicMock(return_value=None)
    mock_method.return_value = operation

    delete_connector.delete_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
    )

    out, _ = capsys.readouterr()
    assert "Deleted connector" in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.pause_connector"
)
def test_pause_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operation = mock.MagicMock(spec=Operation)
    operation.result = mock.MagicMock(return_value=None)
    mock_method.return_value = operation

    pause_connector.pause_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
    )

    out, _ = capsys.readouterr()
    assert "Paused connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.resume_connector"
)
def test_resume_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operation = mock.MagicMock(spec=Operation)
    operation.result = mock.MagicMock(return_value=None)
    mock_method.return_value = operation

    resume_connector.resume_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
    )

    out, _ = capsys.readouterr()
    assert "Resumed connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.stop_connector"
)
def test_stop_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operation = mock.MagicMock(spec=Operation)
    operation.result = mock.MagicMock(return_value=None)
    mock_method.return_value = operation

    stop_connector.stop_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
    )

    out, _ = capsys.readouterr()
    assert "Stopped connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.restart_connector"
)
def test_restart_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    operation = mock.MagicMock(spec=Operation)
    operation.result = mock.MagicMock(return_value=None)
    mock_method.return_value = operation

    restart_connector.restart_connector(
        project_id=PROJECT_ID,
        region=REGION,
        connect_cluster_id=CONNECT_CLUSTER_ID,
        connector_id=CONNECTOR_ID,
    )

    out, _ = capsys.readouterr()
    assert "Restarted connector" in out
    assert CONNECTOR_ID in out
    mock_method.assert_called_once()
