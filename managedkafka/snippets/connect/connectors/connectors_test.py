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
import create_cloud_storage_sink_connector
import create_mirrormaker_connector
import create_pubsub_sink_connector
import create_pubsub_source_connector

PROJECT_ID = "test-project-id"
REGION = "us-central1"
CONNECT_CLUSTER_ID = "test-connect-cluster-id"


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_mirrormaker2_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "MM2_CONNECTOR_ID"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = connector_id
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_mirrormaker_connector.create_mirrormaker_connector(
        PROJECT_ID,
        REGION,
        CONNECT_CLUSTER_ID,
        connector_id,
        "GMK_TOPIC_NAME",
        "source",
        "target",
        "GMK_SOURCE_CLUSTER_DNS",
        "GMK_TARGET_CLUSTER_DNS",
        "1",
        "SASL_SSL",
        "OAUTHBEARER",
        "com.google.cloud.hosted.kafka.auth.GcpLoginCallbackHandler",
        "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;",
        "SASL_SSL",
        "OAUTHBEARER",
        "com.google.cloud.hosted.kafka.auth.GcpLoginCallbackHandler",
        "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;",
    )

    out, _ = capsys.readouterr()
    assert "Created Connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_pubsub_source_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "CPS_SOURCE_CONNECTOR_ID"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = connector_id
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_pubsub_source_connector.create_pubsub_source_connector(
        PROJECT_ID,
        REGION,
        CONNECT_CLUSTER_ID,
        connector_id,
        "GMK_TOPIC_ID",
        "CPS_SUBSCRIPTION_ID",
        "GCP_PROJECT_ID",
        "1",
        "org.apache.kafka.connect.converters.ByteArrayConverter",
        "org.apache.kafka.connect.storage.StringConverter",
    )

    out, _ = capsys.readouterr()
    assert "Created Connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_pubsub_sink_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "CPS_SINK_CONNECTOR_ID"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = connector_id
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_pubsub_sink_connector.create_pubsub_sink_connector(
        PROJECT_ID,
        REGION,
        CONNECT_CLUSTER_ID,
        connector_id,
        "GMK_TOPIC_ID",
        "org.apache.kafka.connect.storage.StringConverter",
        "org.apache.kafka.connect.storage.StringConverter",
        "CPS_TOPIC_ID",
        "GCP_PROJECT_ID",
        "1",
    )

    out, _ = capsys.readouterr()
    assert "Created Connector" in out
    assert connector_id in out
    mock_method.assert_called_once()


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_cloud_storage_sink_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "GCS_SINK_CONNECTOR_ID"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = connector_id
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_cloud_storage_sink_connector.create_cloud_storage_sink_connector(
        PROJECT_ID,
        REGION,
        CONNECT_CLUSTER_ID,
        connector_id,
        "GMK_TOPIC_ID",
        "GCS_BUCKET_NAME",
        "1",
        "json",
        "org.apache.kafka.connect.json.JsonConverter",
        "false",
        "org.apache.kafka.connect.storage.StringConverter",
    )

    out, _ = capsys.readouterr()
    assert "Created Connector" in out
    assert connector_id


@mock.patch(
    "google.cloud.managedkafka_v1.services.managed_kafka_connect.ManagedKafkaConnectClient.create_connector"
)
def test_create_bigquery_sink_connector(
    mock_method: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    connector_id = "BQ_SINK_CONNECTOR_ID"
    operation = mock.MagicMock(spec=Operation)
    connector = managedkafka_v1.types.Connector()
    connector.name = connector_id
    operation.result = mock.MagicMock(return_value=connector)
    mock_method.return_value = operation

    create_bigquery_sink_connector.create_bigquery_sink_connector(
        PROJECT_ID,
        REGION,
        CONNECT_CLUSTER_ID,
        connector_id,
        "GMK_TOPIC_ID",
        "3",
        "org.apache.kafka.connect.storage.StringConverter",
        "org.apache.kafka.connect.json.JsonConverter",
        "false",
        "BQ_DATASET_ID",
    )

    out, _ = capsys.readouterr()
    assert "Created Connector" in out
    assert connector_id in out
    mock_method.assert_called_once()
