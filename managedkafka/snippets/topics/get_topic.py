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

# [START managedkafka_get_topic]
from google.cloud import managedkafka_v1


def get_topic(
    project_id: str,
    region: str,
    cluster_id: str,
    topic_id: str,
) -> managedkafka_v1.Topic:
    """
    Get a Kafka topic.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        topic_id: ID of the Kafka topic.
    """

    client = managedkafka_v1.ManagedKafkaClient()

    topic_path = client.topic_path(project_id, region, cluster_id, topic_id)
    request = managedkafka_v1.GetTopicRequest(
        name=topic_path,
    )

    topic = client.get_topic(request=request)
    print("Got topic:", topic)

    return topic


# [END managedkafka_get_topic]
