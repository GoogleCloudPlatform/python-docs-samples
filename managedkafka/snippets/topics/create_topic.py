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


def create_topic(
    project_id: str,
    region: str,
    cluster_id: str,
    topic_id: str,
    partition_count: int,
    replication_factor: int,
    configs: dict[str, str],
) -> None:
    """
    Create a Kafka topic.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        topic_id: ID of the Kafka topic.
        partition_count: Number of partitions in a topic..
        replication_factor: Number of replicas of each partition.
        configs: Configuration of the topic.

    Raises:
        This method will raise the AlreadyExists exception if the topic already exists.
    """
    # [START managedkafka_create_topic]
    from google.api_core.exceptions import AlreadyExists
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"
    # topic_id = "my-topic"
    # partition_count = 10
    # replication_factor = 3
    # configs = {"min.insync.replicas": "1"}

    client = managedkafka_v1.ManagedKafkaClient()

    topic = managedkafka_v1.Topic()
    topic.name = client.topic_path(project_id, region, cluster_id, topic_id)
    topic.partition_count = partition_count
    topic.replication_factor = replication_factor
    # For a list of configs, one can check https://kafka.apache.org/documentation/#topicconfigs
    topic.configs = configs

    request = managedkafka_v1.CreateTopicRequest(
        parent=client.cluster_path(project_id, region, cluster_id),
        topic_id=topic_id,
        topic=topic,
    )

    try:
        response = client.create_topic(request=request)
        print("Created topic:", response.name)
    except AlreadyExists as e:
        print(f"Failed to create topic {topic.name} with error: {e.message}")

    # [END managedkafka_create_topic]
