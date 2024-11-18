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


def delete_cluster(
    project_id: str,
    region: str,
    cluster_id: str,
) -> None:
    """
    Delete a Kafka cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors or
        the timeout before the operation completes is reached.
    """
    # [START managedkafka_delete_cluster]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"

    client = managedkafka_v1.ManagedKafkaClient()

    request = managedkafka_v1.DeleteClusterRequest(
        name=client.cluster_path(project_id, region, cluster_id),
    )

    try:
        operation = client.delete_cluster(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        operation.result()
        print("Deleted cluster")
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e.message}")

    # [END managedkafka_delete_cluster]
