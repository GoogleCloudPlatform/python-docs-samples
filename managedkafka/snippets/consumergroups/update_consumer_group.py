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


def update_consumer_group(
    project_id: str,
    region: str,
    cluster_id: str,
    consumer_group_id: str,
    topic_path: str,
    partition_offsets: dict[int, int],
) -> None:
    """
    Update a single partition's offset in a Kafka consumer group.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        consumer_group_id: ID of the Kafka consumer group.
        topic_path: Name of the Kafka topic.
        partition_offsets: Configuration of the topic, represented as a map of partition indexes to their offset value.

    Raises:
        This method will raise the NotFound exception if the consumer group or the parent resource is not found.
    """
    # [START managedkafka_update_consumergroup]
    from google.api_core.exceptions import NotFound
    from google.cloud import managedkafka_v1
    from google.protobuf import field_mask_pb2

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"
    # consumer_group_id = "my-consumer-group"
    # topic_path = "my-topic-path"
    # partition_offsets = {10: 10}

    client = managedkafka_v1.ManagedKafkaClient()

    consumer_group = managedkafka_v1.ConsumerGroup()
    consumer_group.name = client.consumer_group_path(
        project_id, region, cluster_id, consumer_group_id
    )

    topic_metadata = managedkafka_v1.ConsumerTopicMetadata()
    for partition, offset in partition_offsets.items():
        partition_metadata = managedkafka_v1.ConsumerPartitionMetadata(offset=offset)
        topic_metadata.partitions[partition] = partition_metadata
    consumer_group.topics = {
        topic_path: topic_metadata,
    }

    update_mask = field_mask_pb2.FieldMask()
    update_mask.paths.append("topics")

    request = managedkafka_v1.UpdateConsumerGroupRequest(
        update_mask=update_mask,
        consumer_group=consumer_group,
    )

    try:
        response = client.update_consumer_group(request=request)
        print("Updated consumer group:", response)
    except NotFound as e:
        print(f"Failed to update consumer group {consumer_group_id} with error: {e.message}")

    # [END managedkafka_update_consumergroup]
