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

def create_mirrormaker2_source_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
    source_bootstrap_servers: str,
    target_bootstrap_servers: str,
    tasks_max: str,
    source_cluster_alias: str,
    target_cluster_alias: str,
    topics: str,
    topics_exclude: str,
) -> None:
    """
    Create a MirrorMaker 2.0 Source connector.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: Name of the connector.
        source_bootstrap_servers: Source cluster bootstrap servers.
        target_bootstrap_servers: Target cluster bootstrap servers. This is usually the primary cluster.
        tasks_max: Controls the level of parallelism for the connector.
        source_cluster_alias: Alias for the source cluster.
        target_cluster_alias: Alias for the target cluster.
        topics: Topics to mirror.
        topics_exclude: Topics to exclude from mirroring.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors.
    """
    # TODO(developer): Update with your config values. Here is a sample configuration:
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "mm2-source-to-target-connector-id"
    # source_bootstrap_servers = "source_cluster_dns"
    # target_bootstrap_servers = "target_cluster_dns"
    # tasks_max = "3"
    # source_cluster_alias = "source"
    # target_cluster_alias = "target"
    # topics = ".*"
    # topics_exclude = "mm2.*.internal,.*.replica,__.*"

    # [START managedkafka_create_mirrormaker2_source_connector]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.cloud.managedkafka_v1.types import Connector, CreateConnectorRequest

    connect_client = ManagedKafkaConnectClient()
    parent = connect_client.connect_cluster_path(project_id, region, connect_cluster_id)

    configs = {
        "connector.class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
        "name": connector_id,
        "tasks.max": tasks_max,
        "source.cluster.alias": source_cluster_alias,
        "target.cluster.alias": target_cluster_alias,  # This is usually the primary cluster.
        # Replicate all topics from the source
        "topics": topics,
        # The value for bootstrap.servers is a hostname:port pair for the Kafka broker in 
        # the source/target cluster.
        # For example: "kafka-broker:9092"
        "source.cluster.bootstrap.servers": source_bootstrap_servers,
        "target.cluster.bootstrap.servers": target_bootstrap_servers,
        # You can define an exclusion policy for topics as follows:
        # To exclude internal MirrorMaker 2 topics, internal topics and replicated topics.
        "topics.exclude": topics_exclude,
    }

    connector = Connector()
    # The name of the connector.
    connector.name = connector_id
    connector.configs = configs

    request = CreateConnectorRequest(
        parent=parent,
        connector_id=connector_id,
        connector=connector,
    )

    try:
        operation = connect_client.create_connector(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        response = operation.result()
        print("Created Connector:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e}")
    # [END managedkafka_create_mirrormaker2_source_connector]
