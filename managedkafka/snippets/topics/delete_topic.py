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


def delete_topic(
    project_id: str,
    region: str,
    cluster_id: str,
    topic_id: str,
) -> None:
    """
    Delete a Kafka topic.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        topic_id: ID of the Kafka topic.

    Raises:
        This method will raise the NotFound exception if the topic or the parent resource is not found.
    """
    # [START managedkafka_delete_topic]
    from google.api_core.exceptions import NotFound
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"
    # topic_id = "my-topic"

    client = managedkafka_v1.ManagedKafkaClient()

    topic_path = client.topic_path(project_id, region, cluster_id, topic_id)
    request = managedkafka_v1.DeleteTopicRequest(name=topic_path)

    try:
        client.delete_topic(request=request)
        print("Deleted topic")
    except NotFound as e:
        print(f"Failed to delete topic {topic_id} with error: {e.message}")

    # [END managedkafka_delete_topic]
