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

# [START managedkafka_update_topic]
from google.api_core.exceptions import NotFound
from google.cloud import managedkafka_v1
from google.protobuf import field_mask_pb2


def update_topic(
    project_id: str,
    region: str,
    cluster_id: str,
    topic_id: str,
    partition_count: int,
    configs: dict[str, str],
) -> None:
    """
    Update a Kafka topic. For a list of editable fields, one can check https://cloud.google.com/managed-kafka/docs/create-topic#properties.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        topic_id: ID of the Kafka topic.
        partition_count: Number of partitions in a topic..
        configs: Configuration of the topic.

    Raises:
        This method will raise the exception if the topic is not found.
    """

    client = managedkafka_v1.ManagedKafkaClient()

    topic = managedkafka_v1.Topic()
    topic.name = client.topic_path(project_id, region, cluster_id, topic_id)
    topic.partition_count = partition_count
    topic.configs = configs
    update_mask = field_mask_pb2.FieldMask()
    update_mask.paths.extend(["partition_count", "configs"])

    request = managedkafka_v1.UpdateTopicRequest(
        update_mask=update_mask,
        topic=topic,
    )

    try:
        response = client.update_topic(request=request)
        print("Updated topic:", response)
    except NotFound:
        print(f"Topic {topic.name} not found")


# [END managedkafka_update_topic]
