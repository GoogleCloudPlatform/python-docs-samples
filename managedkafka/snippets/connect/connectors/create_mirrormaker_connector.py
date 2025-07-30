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


def create_mirrormaker_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
    source_cluster_dns: str,
    target_cluster_dns: str,
    topic_name: str,
) -> None:
    """
    Creates a MirrorMaker 2.0 source connector.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: ID for the new connector.
        source_cluster_dns: DNS name of the source cluster.
        target_cluster_dns: DNS name of the target cluster.
        topic_name: Name of the topic to mirror.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors.
    """
    # [START managedkafka_create_mirrormaker_connector]
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
    # connector_id = "my-mirrormaker-connector"
    # source_cluster_dns = "source-cluster.c.my-project.internal:9092"
    # target_cluster_dns = "target-cluster.c.my-project.internal:9092"
    # topic_name = "my-topic"

    connect_client = ManagedKafkaConnectClient()

    # Here is a sample configuration for the MirrorMaker source connector
    configs = {
        "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
        "name": connector_id,
        "source.cluster.alias": "source",
        "target.cluster.alias": "target",
        "topics": topic_name,
        "source.cluster.bootstrap.servers": source_cluster_dns,
        "target.cluster.bootstrap.servers": target_cluster_dns,
        "offset-syncs.topic.replication.factor": "1",
        "source.cluster.security.protocol": "SASL_SSL",
        "source.cluster.sasl.mechanism": "OAUTHBEARER",
        "source.cluster.sasl.login.callback.handler.class": "com.google.cloud.hosted.kafka.auth.GcpLoginCallbackHandler",
        "source.cluster.sasl.jaas.config": "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;",
        "target.cluster.security.protocol": "SASL_SSL",
        "target.cluster.sasl.mechanism": "OAUTHBEARER",
        "target.cluster.sasl.login.callback.handler.class": "com.google.cloud.hosted.kafka.auth.GcpLoginCallbackHandler",
        "target.cluster.sasl.jaas.config": "org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;"
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
        print("Created MirrorMaker connector:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e}")

    # [END managedkafka_create_mirrormaker_connector]
