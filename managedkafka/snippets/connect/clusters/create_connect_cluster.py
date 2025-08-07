# Copyright 2025 Google LLC
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


def create_connect_cluster(
    project_id: str,
    region: str,
    connect_cluster_id: str,
    kafka_cluster_id: str,
    primary_subnet: str,
    cpu: int,
    memory_bytes: int,
) -> None:
    """
    Create a Kafka Connect cluster.

    Args:
        project_id: Google Cloud project ID.
        region: Cloud region.
        connect_cluster_id: ID of the Kafka Connect cluster.
        kafka_cluster_id: The ID of the primary Managed Service for Apache Kafka cluster.
        primary_subnet: The primary VPC subnet for the Connect cluster workers. The expected format is projects/{project_id}/regions/{region}/subnetworks/{subnet_id}.
        cpu: Number of vCPUs to provision for the cluster. The minimum is 12.
        memory_bytes: The memory to provision for the cluster in bytes. Must be between 1 GiB * cpu and 8 GiB * cpu.

    Raises:
        This method will raise the GoogleAPICallError exception if the operation errors or
        the timeout before the operation completes is reached.
    """
    # [START managedkafka_create_connect_cluster]
    from google.api_core.exceptions import GoogleAPICallError
    from google.cloud import managedkafka_v1
    from google.cloud.managedkafka_v1.services.managed_kafka_connect import ManagedKafkaConnectClient
    from google.cloud.managedkafka_v1.types import ConnectCluster, CreateConnectClusterRequest, ConnectNetworkConfig

    # TODO(developer): Update with your values.
    # project_id = "my-project-id"
    # region = "us-central1"
    # connect_cluster_id = "my-connect-cluster"
    # kafka_cluster_id = "my-kafka-cluster"
    # primary_subnet = "projects/my-project-id/regions/us-central1/subnetworks/default"
    # cpu = 12
    # memory_bytes = 12884901888  # 12 GiB

    connect_client = ManagedKafkaConnectClient()
    kafka_client = managedkafka_v1.ManagedKafkaClient()

    parent = connect_client.common_location_path(project_id, region)
    kafka_cluster_path = kafka_client.cluster_path(project_id, region, kafka_cluster_id)

    connect_cluster = ConnectCluster()
    connect_cluster.name = connect_client.connect_cluster_path(project_id, region, connect_cluster_id)
    connect_cluster.kafka_cluster = kafka_cluster_path
    connect_cluster.capacity_config.vcpu_count = cpu
    connect_cluster.capacity_config.memory_bytes = memory_bytes
    connect_cluster.gcp_config.access_config.network_configs = [ConnectNetworkConfig(primary_subnet=primary_subnet)]
    # Optionally, you can also specify accessible subnets and resolvable DNS domains as part of your network configuration.
    # For example:
    # connect_cluster.gcp_config.access_config.network_configs = [
    #     ConnectNetworkConfig(
    #         primary_subnet=primary_subnet,
    #         additional_subnets=additional_subnets,
    #         dns_domain_names=dns_domain_names,
    #     )
    # ]

    request = CreateConnectClusterRequest(
        parent=parent,
        connect_cluster_id=connect_cluster_id,
        connect_cluster=connect_cluster,
    )

    try:
        operation = connect_client.create_connect_cluster(request=request)
        print(f"Waiting for operation {operation.operation.name} to complete...")
        # Creating a Connect cluster can take 10-40 minutes.
        response = operation.result(timeout=3000)
        print("Created Connect cluster:", response)
    except GoogleAPICallError as e:
        print(f"The operation failed with error: {e}")

    # [END managedkafka_create_connect_cluster]
