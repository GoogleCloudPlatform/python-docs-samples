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


def update_cluster(
    project_id: str, region: str, cluster_id: str, memory_bytes: int
) -> None:
    """
    Update a Kafka cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        memory_bytes: The memory to provision for the cluster in bytes.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors or
        the timeout before the operation completes is reached.
    """
    # [START managedkafka_update_cluster]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud import managedkafka_v1
    from google.protobuf import field_mask_pb2

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"
    # memory_bytes = 4295000000

    client = managedkafka_v1.ManagedKafkaClient()

    cluster = managedkafka_v1.Cluster()
    cluster.name = client.cluster_path(project_id, region, cluster_id)
    cluster.capacity_config.memory_bytes = memory_bytes
    update_mask = field_mask_pb2.FieldMask()
    update_mask.paths.append("capacity_config.memory_bytes")

    # For a list of editable fields, one can check https://cloud.google.com/managed-kafka/docs/create-cluster#properties.
    request = managedkafka_v1.UpdateClusterRequest(
        update_mask=update_mask,
        cluster=cluster,
    )

    try:
        operation = client.update_cluster(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        response = operation.result()
        print("Updated cluster:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e.message}")

    # [END managedkafka_update_cluster]
