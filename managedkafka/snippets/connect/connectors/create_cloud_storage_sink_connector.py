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

def create_cloud_storage_sink_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
    topics: str,
    gcs_bucket_name: str,
    tasks_max: str,
    format_output_type: str,
    value_converter: str,
    value_converter_schemas_enable: str,
    key_converter: str,
) -> None:
    """
    Create a Cloud Storage Sink connector.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: Name of the connector.
        topics: Kafka topics to read from.
        gcs_bucket_name: Google Cloud Storage bucket name.
        tasks_max: Maximum number of tasks.
        format_output_type: Output format type.
        value_converter: Value converter class.
        value_converter_schemas_enable: Enable schemas for value converter.
        key_converter: Key converter class.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors or
        the timeout before the operation completes is reached.
    """
    # TODO(developer): Update with your config values. Here is a sample configuration:
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "GCS_SINK_CONNECTOR_ID"
    # topics = "GMK_TOPIC_ID"
    # gcs_bucket_name = "GCS_BUCKET_NAME"
    # tasks_max = "3"
    # format_output_type = "json"
    # value_converter = "org.apache.kafka.connect.json.JsonConverter"
    # value_converter_schemas_enable = "false"
    # key_converter = "org.apache.kafka.connect.storage.StringConverter"

    # [START managedkafka_create_cloud_storage_sink_connector]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.cloud.managedkafka_v1.types import Connector, CreateConnectorRequest

    connect_client = ManagedKafkaConnectClient()
    parent = connect_client.connect_cluster_path(project_id, region, connect_cluster_id)

    configs = {
        "connector.class": "io.aiven.kafka.connect.gcs.GcsSinkConnector",
        "tasks.max": tasks_max,
        "topics": topics,
        "gcs.bucket.name": gcs_bucket_name,
        "gcs.credentials.default": "true",
        "format.output.type": format_output_type,
        "name": connector_id,
        "value.converter": value_converter,
        "value.converter.schemas.enable": value_converter_schemas_enable,
        "key.converter": key_converter,
    }

    connector = Connector()
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
    # [END managedkafka_create_cloud_storage_sink_connector]
