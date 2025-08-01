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


def create_pubsub_sink_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
    kafka_topic: str,
    pubsub_topic_id: str,
    target_project_id: str = None,
) -> None:
    """
    Creates a Pub/Sub sink connector.

    Args:
        project_id: Google Cloud project ID where the connector will be created.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: ID for the new connector.
        kafka_topic: Name of the Kafka topic to read messages from.
        pubsub_topic_id: ID of the Pub/Sub topic to write messages to.
        target_project_id: Project ID containing the Pub/Sub topic. If not provided,
            uses the same project as the connector.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors.
    """
    # [START managedkafka_create_pubsub_sink_connector]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud import managedkafka_v1
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.cloud.managedkafka_v1.types import Connector

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "my-pubsub-sink"
    # kafka_topic = "my-kafka-topic"
    # pubsub_topic_id = "my-pubsub-topic"
    # target_project_id = "my-target-project"  # Optional

    if target_project_id is None:
        target_project_id = project_id

    connect_client = ManagedKafkaConnectClient()

    # Here is a sample configuration for the Pub/Sub sink connector
    configs = {
        "connector.class": "com.google.pubsub.kafka.sink.CloudPubSubSinkConnector",
        "name": connector_id,
        "tasks.max": "1",
        "topics": kafka_topic,
        "value.converter": "org.apache.kafka.connect.storage.StringConverter",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "cps.topic": pubsub_topic_id,
        "cps.project": target_project_id
    }

    connector = Connector()
    connector.name = connect_client.connector_path(
        project_id, region, connect_cluster_id, connector_id
    )
    connector.configs = configs

    request = managedkafka_v1.CreateConnectorRequest(
        parent=connect_client.connect_cluster_path(project_id, region, connect_cluster_id),
        connector_id=connector_id,
        connector=connector,
    )

    try:
        operation = connect_client.create_connector(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        response = operation.result()
        print("Created Pub/Sub sink connector:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e}")

    # [END managedkafka_create_pubsub_sink_connector]
