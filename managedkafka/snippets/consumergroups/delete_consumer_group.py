# Copyright 2024 Google LLC
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


def delete_consumer_group(
    project_id: str,
    region: str,
    cluster_id: str,
    consumer_group_id: str,
) -> None:
    """
    Delete a Kafka consumer group.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        consumer_group_id: ID of the Kafka consumer group.

    Raises:
        This method will raise the NotFound exception if the consumer group or the parent resource is not found.
    """
    # [START managedkafka_delete_consumergroup]
    from google.api_core.exceptions import NotFound
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"
    # consumer_group_id = "my-consumer-group"

    client = managedkafka_v1.ManagedKafkaClient()

    consumer_group_path = client.consumer_group_path(
        project_id, region, cluster_id, consumer_group_id
    )
    request = managedkafka_v1.DeleteConsumerGroupRequest(
        name=consumer_group_path,
    )

    try:
        client.delete_consumer_group(request=request)
        print("Deleted consumer group")
    except NotFound as e:
        print(f"Failed to delete consumer group {consumer_group_id} with error: {e.message}")

    # [END managedkafka_delete_consumergroup]
