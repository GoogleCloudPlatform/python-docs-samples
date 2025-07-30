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


def list_connectors(
    project_id: str,
    region: str,
    connect_cluster_id: str,
) -> None:
    """
    List all connectors in a Kafka Connect cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
    """
    # [START managedkafka_list_connectors]
    from google.cloud import managedkafka_v1
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.api_core.exceptions import GoogleAPICallError

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"

    connect_client = ManagedKafkaConnectClient()

    request = managedkafka_v1.ListConnectorsRequest(
        parent=connect_client.connect_cluster_path(project_id, region, connect_cluster_id),
    )

    try:
        response = connect_client.list_connectors(request=request)
        for connector in response:
            print("Got connector:", connector)
    except GoogleAPICallError as e:
        print(f"Failed to list connectors with error: {e}")

    # [END managedkafka_list_connectors]
