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


def update_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
    configs: dict,
) -> None:
    """
    Update a connector's configuration.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: ID of the connector.
        config: Dictionary containing the updated configuration.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors.
    """
    # [START managedkafka_update_connector]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud import managedkafka_v1
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.cloud.managedkafka_v1.types import Connector
    from google.protobuf import field_mask_pb2

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "my-connector"
    # configs = {
    #     "tasks.max": "2",
    #     "value.converter.schemas.enable" : "true"
    # }

    connect_client = ManagedKafkaConnectClient()

    connector = Connector()
    connector.name = connect_client.connector_path(
        project_id, region, connect_cluster_id, connector_id
    )
    connector.configs = configs
    update_mask = field_mask_pb2.FieldMask()
    update_mask.paths.append("config")

    # For a list of editable fields, one can check https://cloud.google.com/managed-service-for-apache-kafka/docs/connect-cluster/update-connector#editable-properties.
    request = managedkafka_v1.UpdateConnectorRequest(
        update_mask=update_mask,
        connector=connector,
    )

    try:
        operation = connect_client.update_connector(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        response = operation.result()
        print("Updated connector:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e}")

    # [END managedkafka_update_connector]
