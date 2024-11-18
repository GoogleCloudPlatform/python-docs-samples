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


def create_cluster(
    project_id: str,
    region: str,
    cluster_id: str,
    subnet: str,
    cpu: int,
    memory_bytes: int,
) -> None:
    """
    Create a Kafka cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        cluster_id: ID of the Kafka cluster.
        subnet: VPC subnet from which the cluster is accessible. The expected format is projects/{project_id}/regions{region}/subnetworks/{subnetwork}.
        cpu: Number of vCPUs to provision for the cluster.
        memory_bytes: The memory to provision for the cluster in bytes.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors or
        the timeout before the operation completes is reached.
    """
    # [START managedkafka_create_cluster]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud import managedkafka_v1

    # TODO(developer)
    # project_id = "my-project-id"
    # region = "us-central1"
    # cluster_id = "my-cluster"
    # subnet = "projects/my-project-id/regions/us-central1/subnetworks/default"
    # cpu = 3
    # memory_bytes = 3221225472

    client = managedkafka_v1.ManagedKafkaClient()

    cluster = managedkafka_v1.Cluster()
    cluster.name = client.cluster_path(project_id, region, cluster_id)
    cluster.capacity_config.vcpu_count = cpu
    cluster.capacity_config.memory_bytes = memory_bytes
    cluster.gcp_config.access_config.network_configs = [
        managedkafka_v1.NetworkConfig(subnet=subnet)
    ]
    cluster.rebalance_config.mode = (
        managedkafka_v1.RebalanceConfig.Mode.AUTO_REBALANCE_ON_SCALE_UP
    )

    request = managedkafka_v1.CreateClusterRequest(
        parent=client.common_location_path(project_id, region),
        cluster_id=cluster_id,
        cluster=cluster,
    )

    try:
        operation = client.create_cluster(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        # The duration of this operation can vary considerably, typically taking 10-40 minutes.
        # We can set a timeout of 3000s (50 minutes).
        response = operation.result(timeout=3000)
        print("Created cluster:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e.message}")

    # [END managedkafka_create_cluster]
