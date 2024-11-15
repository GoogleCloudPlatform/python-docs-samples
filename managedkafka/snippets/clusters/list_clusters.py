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


def list_clusters(
    project_id: str,
    region: str,
):
    """
    List Kafka clusters in a given project ID and region.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
    """
    # [START managedkafka_list_clusters]
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"

    client = managedkafka_v1.ManagedKafkaClient()

    request = managedkafka_v1.ListClustersRequest(
        parent=client.common_location_path(project_id, region),
    )

    response = client.list_clusters(request=request)
    for cluster in response:
        print("Got cluster:", cluster)

    # [END managedkafka_list_clusters]
