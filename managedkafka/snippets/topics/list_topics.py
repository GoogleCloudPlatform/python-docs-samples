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


def list_topics(
    project_id: str,
    region: str,
    cluster_id: str,
):
    """
    List Kafka topics in a cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
    """
    # [START managedkafka_list_topics]
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"

    client = managedkafka_v1.ManagedKafkaClient()

    request = managedkafka_v1.ListTopicsRequest(
        parent=client.cluster_path(project_id, region, cluster_id),
    )

    response = client.list_topics(request=request)
    for topic in response:
        print("Got topic:", topic)

    # [END managedkafka_list_topics]
