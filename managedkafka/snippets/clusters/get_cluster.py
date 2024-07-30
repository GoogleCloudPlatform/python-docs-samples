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

# [START managedkafka_get_cluster]
from google.cloud import managedkafka_v1


def get_cluster(
    project_id: str,
    region: str,
    cluster_id: str,
) -> managedkafka_v1.Cluster:
    """
    Get a Kafka cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
    """

    client = managedkafka_v1.ManagedKafkaClient()

    cluster_path = client.cluster_path(project_id, region, cluster_id)
    request = managedkafka_v1.GetClusterRequest(
        name=cluster_path,
    )

    cluster = client.get_cluster(request=request)
    print("Got cluster:", cluster)

    return cluster


# [END managedkafka_get_cluster]
