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


def list_connect_clusters(
    project_id: str,
    region: str,
) -> None:
    """
    List Kafka Connect clusters in a given project ID and region.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
    """
    # [START managedkafka_list_connect_clusters]
    from google.cloud import managedkafka_v1
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import (
        ManagedKafkaConnectClient,
    )
    from google.api_core.exceptions import GoogleAPICallError

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"

    connect_client = ManagedKafkaConnectClient()

    request = managedkafka_v1.ListConnectClustersRequest(
        parent=connect_client.common_location_path(project_id, region),
    )

    response = connect_client.list_connect_clusters(request=request)
    for cluster in response:
        try:
            print("Got Connect cluster:", cluster)
        except GoogleAPICallError as e:
            print(f"Failed to list Connect clusters with error: {e}")

    # [END managedkafka_list_connect_clusters]
