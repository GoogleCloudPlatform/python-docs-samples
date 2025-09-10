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


def get_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
) -> None:
    """
    Get details of a specific connector.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: ID of the connector.

    Raises:
        This method will raise the NotFound exception if the connector is not found.
    """
    # [START managedkafka_get_connector]
    from google.api_core.exceptions import NotFound
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import ManagedKafkaConnectClient
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "my-connector"

    connect_client = ManagedKafkaConnectClient()

    connector_path = connect_client.connector_path(
        project_id, region, connect_cluster_id, connector_id
    )
    request = managedkafka_v1.GetConnectorRequest(
        name=connector_path,
    )

    try:
        connector = connect_client.get_connector(request=request)
        print("Got connector:", connector)
    except NotFound as e:
        print(f"Failed to get connector {connector_id} with error: {e}")

    # [END managedkafka_get_connector]
