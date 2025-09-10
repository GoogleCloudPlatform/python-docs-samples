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


def resume_connector(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    connector_id: str,
) -> None:
    """
    Resume a paused connector.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        connector_id: ID of the connector.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors.
    """
    # [START managedkafka_resume_connector]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # connector_id = "my-connector"

    connect_client = ManagedKafkaConnectClient()

    request = managedkafka_v1.ResumeConnectorRequest(
        name=connect_client.connector_path(project_id, region, connect_cluster_id, connector_id),
    )

    try:
        operation = connect_client.resume_connector(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result()
        print(f"Resumed connector {connector_id}")
    except GoogleAPICallError as e:
        print(f"Failed to resume connector {connector_id} with error: {e}")

    # [END managedkafka_resume_connector]
